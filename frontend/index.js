document.addEventListener('submit', async (event) => {
    if (event.target.classList.contains('comment-form')) {
        event.preventDefault(); // Prevent the form from submitting in the traditional way

        const form = event.target;
        const postId = form.dataset.postId;
        const commentInput = form.querySelector('.comment-input');
        const text = commentInput.value.trim();

        if (!text) {
            alert("Please enter a comment.");
            return;
        }

        const userId = localStorage.getItem('userId'); // Get the user ID from local storage

        try {
            const response = await fetch('http://127.0.0.1:5001/add_comment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    post_id: postId,
                    user_id: userId,
                    text: text
                })
            });

            const result = await response.json();

            if (response.status === 201) {
                // Comment added successfully!
                commentInput.value = ''; // Clear the input field
                loadFeed(); // Refresh the feed to display the new comment (or just refresh the comments for that post)
            } else {
                // Display an error message
                alert(result.message);
            }
        } catch (error) {
            console.error("Error adding comment:", error);
            alert("Failed to add comment. Please try again later.");
        }
    }
});
