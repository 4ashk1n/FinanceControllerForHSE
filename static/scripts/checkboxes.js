function CheckBoxCategorie(color, elem, autochange=true) {
    /*
    Функция для переключения разноцветных чекбоксов категорий
    - color: цвет категории
    - elem: ссылка на чекбокс
    - autochange: автоприменение фильтров вкл/выкл
     */
    if(elem.checked){
        elem.style.backgroundColor=color;
    }
    else{elem.style.background='';}
    if(autochange){
        FiltersRender();
    }
}