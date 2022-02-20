function PopupWindowShow(id, name, color) {
    /*
    Функция для показа всплывающего окна
    - id: идентификатор категории
    - name: название категории
    - color: цвет категории
     */
    document.getElementById("dim").style.display = "inline-block";
    document.getElementById("popup").style.display = "inline-block";
    document.getElementById("popup_close").style.display = "inline-block";
    document.getElementById("popup_color_input").value = color;
    document.getElementById("popup_name_input").value = name;
    document.getElementById("popup_id").value = id;
}
function PopupWindowHide() {
    /*
    Функция для скрытия всплывающего окна
     */
    document.getElementById("dim").style.display = "none";
    document.getElementById("popup").style.display = "none";
    document.getElementById("popup_close").style.display = "none";
}
