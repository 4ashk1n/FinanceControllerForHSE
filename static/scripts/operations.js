function PopupWindowShow(date, amountbig=0, amounsmall=0, description="", color, id_, type, category_name) {
    // alert(`operation_${id_}`);
    // alert(document.getElementById(`operation_${id_}`));
    if(BaseMode){
        BaseChange(id_, amountbig, amounsmall)
        return;
    }

    if(date === ''){
        let today = new Date();
        date = today.toISOString().slice(0, -8) + ":00";
    }
    document.getElementById("dim").style.display = "inline-block";
    document.getElementById("popup").style.display = "inline-block";
    document.getElementById("popup_close").style.display = "inline-block";
    document.getElementById("popup_color").style.backgroundColor = color
    document.getElementById("popup_text").innerText = category_name;
    let sign = '-';
    if(type){
        sign='+';
        document.getElementById("popup_amount_big").style.color = '#008e00';
        document.getElementById("popup_amount_small").style.color = '#008e00';
    }
    document.getElementById("popup_amount_big").innerText = sign + amountbig;
    document.getElementById("popup_amount_small").innerText = ','+amounsmall;
    document.getElementById("popup_date").innerText = date;
    document.getElementById("popup_description_text").innerText = `${description}`;
    document.getElementById('popup_op_id').innerHTML = id_
    // console.log(document.getElementById("popup_button_edit").onclick.)
    // console.log(type)
    // document.getElementById("popup_button_edit").onclick =
    //     document.getElementById("popup_button_edit").onclick.replace('0', type)
    // document.getElementById("popup_button_edit").onclick =
    //     document.getElementById("popup_button_edit").onclick.replace('1', type)


}
function PopupWindowHide(ctgs) {
    EditMode = false;
    document.getElementById("dim").style.display = "none";
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup_close").style.display = "none";
    PopupReset(ctgs);
}
function FiltersRender(){
    try{
        let filtered_categories = [];
        let cats_filter = document.getElementsByClassName("categorie_checkbox");
        for(let cat of cats_filter) {
            if (cat.checked && cat.name.includes("categorie")) {
                filtered_categories.push(Number(cat.name.split('_')[1]));
            }
        }
        let operations = document.getElementsByClassName("operation")
        let date_start = null;
        if(document.getElementById("date_start").value) {
            date_start = new Date(
                    document.getElementById("date_start").value.toString() + " UTC+3"
            )
        }
        else{
            date_start = new Date(1970, 1, 1, 0, 0, 0);
        }


        let date_end = null;
        if(document.getElementById("date_end").value){
            date_end = new Date(
                    document.getElementById("date_end").value.toString() + " UTC+3"
            )
            date_end.setDate(date_end.getDate() + 1);
            date_end.setSeconds(date_end.getSeconds() - 1);
        }
        else{
            date_end = new Date(2100, 12, 31, 23, 59, 59);
        }

        let type0 = document.getElementById("type_0").checked;
        let type1 = document.getElementById("type_1").checked;

        try{
            for(let op of operations){
                // console.log(filtered_categories.includes(Number(op.getAttribute("data-categorie").split('_')[1])))
                let op_date = new Date(op.getAttribute("data-date"));
                // console.log("<end ", op_date.getTime() <= date_end.getTime());
                // console.log(">start", op_date.getTime() >= date_start.getTime());
                // console.log(op_date, date_start, date_end);
                if(op_date.getTime() <= date_end.getTime() && op_date.getTime() >= date_start.getTime() &&
                    filtered_categories.includes(Number(op.getAttribute("data-categorie"))) &&
                        (op.getAttribute("data-type") === "1" && type1 ||
                        op.getAttribute("data-type") === "0" && type0)){
                    op.style.display = "inline-block"
                }
                else{
                    op.style.display = "none";
                }
            }
        }
        catch (e) {
            alert(e);
        }


        let tables = document.getElementsByClassName("ops_table_cont");
        for(let table of tables){
            let local_ops = table.getElementsByClassName("operation");
            let hide = true;

            for(let op of local_ops){
                // alert(op.style.display);
                if(op.style.display !== "none"){
                    hide = false;
                    break;
                }
            }
            if(hide){
                table.style.display = 'none';
            }
            else{
                table.style.display = 'inline-block';
            }
        }
    }
    catch (e) {
        console.log(e);
    }

}
let EditMode = false;

function PopupEdit(ctgs) {
    // alert(document.getElementById("popup_amount_big").innerHTML.slice(1).replaceAll(' ',''))
    if(EditMode){PopupReset(ctgs); return;}
    // alert(document.getElementById("popup_date").value)
    EditMode = true;

    let old_date = 0;
    let old_color = document.getElementById("popup_color").style.backgroundColor
    let edit_onclick = document.getElementById('popup_button_edit').getAttribute('onclick')
    let op_type = document.getElementById("popup_amount_big").innerText.includes("+");

    let opts = ``
    for(ctg of ctgs){
        let checked = document.getElementById("popup_text").innerText === ctg[2] ? "selected" : "";
        opts += `
        <option class="popup_options" value=${ctg[0]} ${checked}>${ctg[2]}</option>`
    }

     let amount_type = `
        <div class="form_radio_btn">
            <input id="popup_amount_plus" type="radio" name="popup_amount_plus" value="1" 
            ${op_type ? "checked" : ""}>
            <label for="popup_amount_plus">+</label>
        </div>
        <br> <br>
        <div class="form_radio_btn">
            <input id="popup_amount_minus" type="radio" name="popup_amount_plus" value="0"
            ${op_type ? "" : "checked"}>
            <label for="popup_amount_minus">-</label>
        </div>
    `

    document.getElementById("popup").innerHTML = `
    <form class="popup_form" id="popup_form" method="post">
        <input id="popup_op_id" name="popup_op_id" style="display: none" value="${document.getElementById('popup_op_id').innerHTML}">
        <div class="popup_top_color" id="popup_color"></div>
        <select class="popup_text" name="popup_ctg" id="popup_ctg" required>
         ${opts}
         </select>
        <div class="popup_amount_cont" id="popup_amount_cont">
       
            <input type="number" class="popup_amount_small" id="popup_amount_small" name="popup_amount_small" min="0" max="99" required
                       value="${document.getElementById("popup_amount_small").innerHTML.slice(1).replaceAll(' ', '')}">
            <input type="number" class="popup_amount_big" id="popup_amount_big"  required min="0" max="99999999" name="popup_amount_big"
                       value="${document.getElementById("popup_amount_big").innerHTML.slice(1).replaceAll(' ','')}">
    
            ${amount_type}
    
            
             
            
        </div>
        <div class="popup_description">
            <textarea class="popup_description_text" id="popup_description_text" name="popup_description_text">
${document.getElementById("popup_description_text").innerHTML}</textarea>
        </div>
        <input required type="datetime-local" class="popup_date" id="popup_date" name="popup_date"
        value=${document.getElementById("popup_date").innerHTML.replace(' ','T')}>
        <div class="popup_buttons">

            <button type="submit" value="" class="popup_button" id="popup_button_confirm"
             name="popup_button_edit">
            </button>
            
            <button class="popup_button" id="popup_button_edit" 
             onclick="${edit_onclick}" style="display: none;">
            </button>
            
        </div>
    </form>`
    document.getElementById('popup_button_confirm').style.backgroundImage = 'url(\'/static/icons/done_black_24dp.svg\')'
    document.getElementById("popup_color").style.backgroundColor = color
    // document.body.appendChild(document.getElementById('popup_form'));
}
function PopupReset(ctgs) {
    EditMode = false;
    edit_onclick = document.getElementById('popup_button_edit').getAttribute('onclick');
    document.getElementById("popup").innerHTML = `
                <div id="popup_op_id" style="display: none;"></div>
				<div class="popup_top_color" id="popup_color"></div>
				<div class="popup_text" id="popup_text"></div>
				<div class="popup_amount_cont" id="popup_amount_cont">
					<span class="popup_amount_small" id="popup_amount_small"></span>
					<span class="popup_amount_big" id="popup_amount_big"></span>
				</div>
				<div class="popup_description">
					<p class="popup_description_text" id="popup_description_text"></p>
				</div>
				<span class="popup_date" id="popup_date"></span>
				<div class="popup_buttons">
					<button class="popup_button" id="popup_button_edit" 
					onclick="${edit_onclick}">
<!--						<img src="icons/edit_black_48dp.svg" alt="None" class="popup_button_edit_img">-->
					</button>
				</div>
    `;

}

let BaseMode = false;
let Base = 1;
let BaseId = -1;

function BaseModeSwitch() {
    // document.getElementById("base_filter_button").checked =
    //     !document.getElementById("base_filter_button").checked;
    if (BaseMode){
        document.getElementById("base_filter_button").checked = false;
    }
    BaseMode = !BaseMode;
    // alert(BaseMode)
    if(!BaseMode){
        BaseChange(-1, 1, 0)
    }
}

function BaseChange(id, amountbig, amountsmall) {
    Base = Number((amountbig + '.' + amountsmall).replaceAll(' ',''));
    if(Base === 0){
        alert("Нельзя использовать операцию стоимостью 0 в качестве базовой")
        return
    }
    if(BaseId !== -1){
        document.getElementById(`operation_${BaseId}`).style.removeProperty('background-color');
    }
    BaseId = id;
    if(BaseId !== -1){
        document.getElementById(`operation_${BaseId}`).style.backgroundColor = '#c8d8f5';
    }
    let ops = document.getElementsByClassName('operation');
    for(let op of ops){
        let am_big_minus = op.getElementsByClassName("op_amount_minus_big")
        let am_small_minus = op.getElementsByClassName("op_amount_minus_small")

        let am_big_plus = op.getElementsByClassName("op_amount_plus_big")
        let am_small_plus = op.getElementsByClassName("op_amount_plus_small")

        let sign = null;
        let am_big = null;
        let am_small = null;

        if(am_big_minus[0]){
            sign = '-';
            am_big = am_big_minus[0];
            am_small = am_small_minus[0];
        }
        else{
            sign = '+';
            am_big = am_big_plus[0];
            am_small = am_small_plus[0];
        }

        let old_amount = op.getAttribute('data-amount');
        let new_amount = null;
        // console.log(old_amount)
        if(BaseId !== -1){
            new_amount = String((Number((old_amount)
                .replaceAll(' ', ''))
                / Base)
                .toFixed(5))
                .split('.');
        }
        else{
            new_amount = String((Number((old_amount)
                .replaceAll(' ', ''))
                / Base)
                .toFixed(2))
                .split('.');
        }



        am_big.innerText = sign + new_amount[0];
        am_small.innerText = ',' + new_amount[1];

    }

    let new_balance = null;
    let old_balance = document.getElementsByClassName("balance_amount")[0]
        .getAttribute('data-amount')

    if(BaseId !== -1){
        new_balance = String((Number((old_balance)
            .replaceAll(' ', '')
                .replace(',','.'))
            / Base)
            .toFixed(5))
            .split('.');
    }
    else{
        new_balance = String((Number((old_balance)
            .replaceAll(' ', '')
                .replace(',','.'))
            / Base)
            .toFixed(2))
            .split('.');
    }

    document.getElementsByClassName("balance_amount_big")[0].innerText =
        new_balance[0];
    document.getElementsByClassName("balance_amount_small")[0].innerText =
        "," + new_balance[1];

}