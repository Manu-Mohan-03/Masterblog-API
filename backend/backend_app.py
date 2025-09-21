from logging import raiseExceptions

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

# Global POST for sake of testing, can be moved to persistent storage as improvement
POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


def validate_blog(blog_post):
    """Validation to check blog contains title and author"""
    if not blog_post.get('title'):
        raise Exception("Title missing")
    if not blog_post.get('content'):
        raise Exception("Content missing")
    return True


def clean_blog(blog_post):
    """To remove unnecessary items from blog post in case user sends
        more element in json apart from title and content"""
    filtered_blog = {}
    if blog_post.get('title'):
        filtered_blog['title'] = blog_post.get('title')
    if blog_post.get('content'):
        filtered_blog['content'] = blog_post.get('content')
    return filtered_blog


def get_post_by_id(post_id):
    """loop and find the blog post belonging to a particular ID"""
    for post in POSTS:
        if post['id'] == post_id:
            return post
    return None

@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    """
    1. Read all the posts using GET request
    2. Query string sort and direction to sort the post
    3. Post request to create a new post
    """
    if request.method == 'POST':
        #get the data from post request
        blog_post = request.get_json()

        # Validate the new post
        try:
            validate_blog(blog_post)
        except Exception as error:
            return jsonify({"error": str(error)}), 400
        blog_post = clean_blog(blog_post)
        #Create new id
        if POSTS:
            new_id = max([post['id'] for post in POSTS]) + 1
        else: # Added as bug fix to handle the case; if all posts got deleted
            new_id = 1
        blog_post['id'] = new_id

        # Add post to blogs list
        POSTS.append(blog_post)
        return jsonify(blog_post), 201
    else:    # Handle Get request
        # retrieve the query parameters
        sort = request.args.get('sort', None)
        direction = request.args.get('direction', None)
        if sort in ('title', 'content') and direction in ('asc', 'desc'):
            # To keep the original intact
            results = POSTS.copy()
            #if not direction or direction == 'asc':
                # if direction not mentioned by default ascending
            if direction == 'asc':
                results.sort(key=lambda post: post.get(sort, ''))
            elif direction == 'desc':
                # to sort in descending order
                results.sort(reverse=True , key=lambda post: post.get(sort, ''))
            return jsonify(results)
        return jsonify(POSTS)


@app.route('/api/posts/<int:post_id>', methods =['DELETE'])
def delete_post(post_id):
    """DELETE API for deleting a blog"""
    blog_post = get_post_by_id(post_id)
    if not blog_post:
        return jsonify({"error": "Not found"}), 404
    POSTS.remove(blog_post)
    return jsonify({"message": f"Post with id {post_id} deleted successfully"})


@app.route('/api/posts/<int:post_id>', methods =['PUT'])
def update_post(post_id):
    """PUT API to update a blog post"""
    blog_post = get_post_by_id(post_id)
    if not blog_post:
        return jsonify({"error": "Not found"}), 404
    # get the data from body of the request
    new_post = request.get_json()
    # Keep only title and content in the new_post
    new_post = clean_blog(new_post)
    # To check if new_post is a subset of existing post (exising post contain post_id,
    # may of may not contain post_id)
    if new_post.items() <= blog_post.items():
        return jsonify({"info": "Nothing to update"})
    blog_post.update(new_post)

    return jsonify(blog_post)


@app.route('/api/posts/search')
def search_post():
    """
    For searching a post using title or content
    Search will return or contents not and contents
    For eg: title=ab&content=cd will show all posts with title 'ab' and
    all the posts with content 'cd'. it will not restrict to only show
    the post with title ab and content cd.
    """
    title = request.args.get('title', None)
    content = request.args.get('content', None)
    result = []
    for post in POSTS:
        print(post)
        if title and title.lower() in post['title'].lower():
            result.append(post)
        if content and content.lower() in post['content'].lower():
            result.append(post)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
