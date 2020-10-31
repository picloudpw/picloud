let MASONRY = null;

document.addEventListener("DOMContentLoaded", function () {

    const grid = document.querySelector('#posts_container');
    clear_posts_container(grid);
    MASONRY = new Masonry(grid, {
        itemSelector: ".post",
        columnWidth: ".post-size-reference",
        gutter: ".post-grid-gutter-size-reference",
        percentPosition: true,
    });
    imagesLoaded(grid).on('progress', () => {
        MASONRY.layout();
    });

    init_posts_search(
        (result, response) => {
            display_post(result['post_id']);
        });

    load_posts_list();


});

function load_posts_list() {
    let container = document.getElementById('posts_container');
    container.classList.add('loading');
    axios.get('/posts/search')
        .then((response) => {
            let posts = response.data['posts'];
            for (let post of posts) {
                append_post(post, container);
            }
        })
        .finally(() => {
            container.classList.remove('loading');
        })
}

function render_post(post) {
    let element = document.createElement("article");
    element.classList.add("post");
    element.innerHTML = `
            <div class="post-container" id="post-${post['id']}">
                <header>
                    <h2>
                        <a onclick="display_post('${post['id']}')" style="cursor: pointer;">${post['title']}</a>
                        ${post['parent_post'] ? '<i class="ui archive icon" title="There is parent post"></i>' : ''}
                    </h2>
                    <p class="subject">
                        <span class="type">${post['type']['title']}</span>
                        |
                        <a class="subject" href="" title="${post['subject']['name']}">
                            ${post['subject']['name']} 
                            <sup>${post['subject']['semester'] > 0 ? post['subject']['semester'] : ''}</sup>
                        </a>
                    </p>
                </header>
                <hr/>
                ${post['html'] ? `<div class="text">${post['html']}</div> <hr/>` : ''}
                
                ${post['image'] ? `
                    <img class="post-img" 
                         ratio="${post['image']['width']}x${post['image']['height']}"
                         src="${post['image']['url']}" 
                         alt="${post['image']['url']}">
                ` : ''}
                
                ${post['link'] ? `
                    <a class="ui primary right labeled icon button btn-follow-link" href="${post['link']}" target="_blank">
                        Open link <i class="angle double right icon"></i>
                    </a>
                ` : ''}

                ${post['file'] ? `
                    <a class="ui green right labeled icon button btn-download" href="${post['file']['url']}">
                        Download '<strong>${post['file']['extension']}</strong>' file <i class="download icon"></i>
                    </a>
                ` : ''}
                
                ${post['is_parent'] ? `
                    <br> <a class="ui button" href="">Child posts</a>
                ` : ''}
                
                <hr/>
                <footer>
                    <a class="post-author" title="Author" href="/students?id=${post['author']['id']}">
                        ${post['author']['user']['username']}
                    </a>
                    <span class="post-created-date">
                        • <span title="Created date and time">${post['created_date_human']}</span>
                    </span>
                    <span class="post-footer-badges">
                        <span class="ui" style="color: #999999" title="Views count">
                            <i class="eye icon"></i>${post['views']}
                        </span>
                        ${post['comments'] ? `
                            <a class="comments-counter" href="">
                                <i class="comment icon" title="Comments count"></i> ${post['comments']}
                            </a>
                        ` : ''}
                    </span>
                </footer>
            </div>
    `;
    return element;
}

function display_post(post_id) {
    let postsGrid = document.getElementById("posts_container");
    axios.get(`/posts/search?id=${post_id}`)
        .then((response) => {
            let posts = response.data['posts'];
            clear_posts_container(postsGrid);
            for (let post of posts) {
                append_post(post, postsGrid);
            }
        })

}

function clear_posts_container(postsGrid) {
    postsGrid.innerHTML = '';

    let masonrySizer = document.createElement("div");
    masonrySizer.classList.add("post-size-reference");
    postsGrid.appendChild(masonrySizer);

    let gutterSizer = document.createElement("div");
    gutterSizer.classList.add("post-grid-gutter-size-reference");
    postsGrid.appendChild(gutterSizer);
}

function append_post(post, postsContainer) {
    let postElement = render_post(post);
    postsContainer.appendChild(postElement);
    MASONRY.appended(postElement);
    imagesLoaded(postElement).on('progress', () => {
        MASONRY.layout();
    });
}
