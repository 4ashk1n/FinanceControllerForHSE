function PopupWindowShow(id, name, color) {
    document.getElementById("dim").style.display = "inline-block";
    document.getElementById("popup").style.display = "inline-block";
    document.getElementById("popup_close").style.display = "inline-block";
    document.getElementById("popup_color_input").value = color;
    document.getElementById("popup_name_input").value = name;
    document.getElementById("popup_id").value = id;
}
function PopupWindowHide(ctgs) {
    document.getElementById("dim").style.display = "none";
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup_close").style.display = "none";
}
