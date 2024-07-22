document.addEventListener('DOMContentLoaded', () => {
    const postForm = document.getElementById('post-form');
    const blogPostsDiv = document.getElementById('blog');

    // Function to display posts
    function displayPosts() {
        blogPostsDiv.innerHTML = '';
        let posts = JSON.parse(localStorage.getItem('posts')) || [];
        posts.forEach((post, index) => {
            const postDiv = document.createElement('div');
            postDiv.className = 'post';
            postDiv.innerHTML = `
                <h3>${post.title}</h3>
                <p>${post.content}</p>
                <button onclick="editPost(${index})">Edit</button>
                <button onclick="deletePost(${index})">Delete</button>
                <div class="comments">
                    <h4>Comments</h4>
                    <div class="comment-list" id="comments-${index}">
                        ${post.comments.map(comment => `<p>${comment}</p>`).join('')}
                    </div>
                    <form class="comment-form" onsubmit="addComment(event, ${index})">
                        <input type="text" placeholder="Add a comment" required>
                        <button type="submit">Add Comment</button>
                    </form>
                </div>
            `;
            blogPostsDiv.appendChild(postDiv);
        });
    }

    // Initial display of posts
    displayPosts();

    // Form submission event listener
    postForm.addEventListener('submit', (event) => {
        event.preventDefault();

        const title = document.getElementById('title').value;
        const content = document.getElementById('content').value;
        const newPost = { title, content, comments: [] };

        let posts = JSON.parse(localStorage.getItem('posts')) || [];
        posts.push(newPost);
        localStorage.setItem('posts', JSON.stringify(posts));

        document.getElementById('title').value = '';
        document.getElementById('content').value = '';
        displayPosts();
    });

    // Global functions for editing and deleting posts
    window.editPost = function(index) {
        let posts = JSON.parse(localStorage.getItem('posts')) || [];
        const post = posts[index];

        document.getElementById('title').value = post.title;
        document.getElementById('content').value = post.content;

        posts.splice(index, 1);
        localStorage.setItem('posts', JSON.stringify(posts));

        displayPosts();
    }

    window.deletePost = function(index) {
        let posts = JSON.parse(localStorage.getItem('posts')) || [];
        posts.splice(index, 1);
        localStorage.setItem('posts', JSON.stringify(posts));
        displayPosts();
    }

    window.addComment = function(event, postIndex) {
        event.preventDefault();
        const commentInput = event.target.querySelector('input');
        const comment = commentInput.value;

        let posts = JSON.parse(localStorage.getItem('posts')) || [];
        posts[postIndex].comments.push(comment);
        localStorage.setItem('posts', JSON.stringify(posts));

        commentInput.value = '';
        displayPosts();
    }
});
