function CheckBoxCategorie(color, elem, autochange=true) {
    // alert(1);
    if(elem.checked){
        elem.style.backgroundColor=color;
    }
    else{elem.style.background='';}
    if(autochange){
        FiltersRender();
    }
}