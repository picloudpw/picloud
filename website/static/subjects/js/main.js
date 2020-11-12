document.addEventListener("DOMContentLoaded", function () {

    restore_state();

});

let SUBJECT_ID = null;

function save_state() {
    let state = {};
    if (SUBJECT_ID) {
        state = {
            "id": SUBJECT_ID,
        };
    }
    push_state(state);
}

function restore_state() {
    let params = new URLSearchParams(document.location.search);

    SUBJECT_ID = params.get("id");

    if (SUBJECT_ID) {
        init_page(SUBJECT_ID);
    } else {

    }

}

function init_page() {
    let container = document.getElementById('subjects_container');
    container.innerHTML = `
        <div class="seven wide column">
            <div class="ui segment" id="hierarchy" style="min-height: 80px"></div>
            <div class="ui segment" id="subject" style="min-height: 80px"></div>
            <div class="ui segment" id="posts" style="min-height: 80px"></div>
        </div>
    `;
    display_subject(document.getElementById('subject'));
    display_posts(document.getElementById('posts'));
}

function display_subject(container) {
    container.classList.add('loading');
    axios.get(`/hierarchy/subjects/get?id=${SUBJECT_ID}`)
        .then((response) => {
            let subject = response.data['subject'];
            container.innerHTML = `
                ${subject['name']} (${subject['semester']})
            `;
            display_department_hierarchy(
                document.getElementById('hierarchy'),
                subject['departments'][0]['id']
            )
        })
        .finally(()=>{
            container.classList.remove('loading');
        })
}

function display_posts(container) {
    container.classList.add('loading');
    axios.get(`/posts/search?subject_id=${SUBJECT_ID}`)
        .then((response) => {
            let posts = response.data['posts'];
            for (let post of posts) {
                container.innerHTML += `
                    <a href="/posts?id=${post['id']}">${post['title']}</a>
                    <div class="ui divider"></div>
                `;
            }
        })
        .finally(()=>{
            container.classList.remove('loading');
        })
}