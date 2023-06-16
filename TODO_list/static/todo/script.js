function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function changeButtonText(todoId, result) {
    var button = document.getElementById("change_button_" + todoId);
    if (result){
        button.innerHTML = 'hotovo';
    }else{
        button.innerHTML = 'nehotovo';
    }
}

function changeTodo(todoId) {
    var csrftoken = getCookie('csrftoken');  // Získání CSRF tokenu z cookies
    var button = $("#change_button_" + todoId);
    button.prop("disabled", true);  // Znefunkční tlačítko
    $.ajax({
        type: "POST",
        url: "/todo/home/api/change_todo",
        headers: {
            "X-CSRFToken": csrftoken  // Zahrnutí CSRF tokenu v hlavičce požadavku
        },
        data: {
            // Případné další data, která chcete odeslat
            "id": todoId
        },
        success: function(response) {
            // Obsluha úspěšné odpovědi
            changeButtonText(todoId,response["result"])
            refresh_status()
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseJSON["error"])
        },
        complete: function() {
            button.prop("disabled", false);  // Opětovné povolení tlačítka
        }
    });
}

function deleteTodoDiv(todoId) {
    var div = document.getElementById("div_" + todoId);
    div.remove();
}

function deleteTodo(todoId) {
    var csrftoken = getCookie('csrftoken');  // Získání CSRF tokenu z cookies
    var button = $("#delete_button_" + todoId);
    button.prop("disabled", true);  // Znefunkční tlačítko
    $.ajax({
        type: "POST",
        url: "/todo/home/api/delete_todo",
        headers: {
            "X-CSRFToken": csrftoken  // Zahrnutí CSRF tokenu v hlavičce požadavku
        },
        data: {
            // Případné další data, která chcete odeslat
            "id": todoId
        },
        success: function(response) {
            // Obsluha úspěšné odpovědi
            deleteTodoDiv(todoId)
            refresh_status()
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseJSON["error"])
        },
        complete: function() {
            button.prop("disabled", false);  // Opětovné povolení tlačítka
        }
    });
}

function refresh_status() {
    var csrftoken = getCookie('csrftoken');  // Získání CSRF tokenu z cookies
    $.ajax({
        type: "POST",
        url: "/todo/home/api/get_status",
        headers: {
            "X-CSRFToken": csrftoken  // Zahrnutí CSRF tokenu v hlavičce požadavku
        },
        data: {
            // Případné další data, která chcete odeslat
        },
        success: function(response) {
            // Obsluha úspěšné odpovědi
            var paragraph = document.querySelector("#status_div p");
            paragraph.textContent = "Počet nesplněných úkolů " + response["count_of_not_done"];
        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(xhr.responseJSON["error"])
        },
        complete: function() {

        }
    });
}