$(document).ready(function () {
    clear_and_disabled_all_elements();
    get_all_universities();
    document.getElementById("id_university").addEventListener("change", function () {
        university_updated(document.getElementById("id_university").value);
    });
    document.getElementById("id_department").addEventListener("change", function () {
        department_updated(document.getElementById("id_department").value);
    });
    document.getElementById("id_chair").addEventListener("change", function () {
        chair_updated(document.getElementById("id_chair").value);
    });
    document.getElementById("id_program").addEventListener("change", function () {
        program_updated(document.getElementById("id_program").value);
    });
    document.getElementById("id_type").options[0].textContent = "Любой";
});

function post_to_html(item) {
    date = new Date(item.created_date)
        .toLocaleString("ru", {
            year: 'numeric',
            month: 'long',
            day: 'numeric',
            hour: 'numeric',
            minute: 'numeric'
        });

    let image, file;
    if (item.image !== "")
        image = " <img src=" + item.image + " class='post-img'>";
    else
        image = "";
    if (item.file !== "")
        file = "<a href='" + item.file + "'> <div class='btn btn-success full-width'>Прикепленный файл</div></a>";
    else
        file = "";

    return "<div class='search-post-panel'> " +
        "<a target='_blank' href='/post/" + item.id + "/'><h4>" + item.title + "</h4> </a>" +
        "<div class='post-text'><p>" + item.text + "</p></div>" +
        image +
        file +
        "<table class='table'> <tr>" +
        "<td>" + item.author_username + "</td>" +
        "<td><a href='/subject/" + item.subject_id + "'>" + item.subject_short_title + "</td>" +
        "<td>" + item.type_title + "</td>" +
        "<td>" + date + "</td>" +
        "<td> <span style='font-size:12px;' class='showopacity glyphicon glyphicon-eye-open'></span>" + item.views + "</td> " +
        "</tr></table>" +
        "</div>"
}

function update_post_list(posts) {
    $("#search_results").empty();
    if (posts.length !== 0) {
        posts.forEach(function (item, i, arr) {
            $('#search_results').append(post_to_html(item));
        });
        update_markdown();
    } else {
        $('#search_results').append("<div class='search-post-panel' style='padding: 10px;'>К сожалению, по вашему запросу ничего не найдено :(</div>");
    }
}

function get_current_values() {
    let university_id;
    let department_id;
    let chair_id;
    let program_id;
    let subject_id;
    let type_id;
    if ($("#id_university").prop('disabled') === false)
        university_id = $("#id_university").val();
    if ($("#id_department").prop('disabled') === false)
        department_id = $("#id_department").val();
    if ($("#id_chair").prop('disabled') === false)
        chair_id = $("#id_chair").val();
    if ($("#id_program").prop('disabled') === false)
        program_id = $("#id_program").val();
    if ($("#id_subject").prop('disabled') === false)
        subject_id = $("#id_subject").val();
    if ($("#id_type").val() !== '')
        type_id = $("#id_type").val();
    return {
        "university_id": university_id,
        "department_id": department_id,
        "chair_id": chair_id,
        "program_id": program_id,
        "subject_id": subject_id,
        "type_id": type_id
    };
}

function new_search_request(data) {
    $.ajax({
        url: "/api/posts/",
        data: data,
        dataType: 'json',
        success: function (data) {
            update_post_list(data);
        }
    });
}

$("#id_type").change(function () {
    new_search_request(get_current_values());
});

$("#id_subject").change(function () {
    new_search_request(get_current_values());
});

function search_posts() {
    let search_request = $("#search-line").find("input").val().toLowerCase();
    $.ajax({
        url: "/api/search_posts/",
        data: {"search_request": search_request},
        dataType: 'json',
        success: function (data) {
            update_post_list(data);
        }
    });
}
