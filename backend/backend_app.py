from logging import raiseExceptions

from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 10, "title": "First post", "content": "This is the first post."},
    {"id": 20, "title": "Second post", "content": "This is the second post."},
]


def validate_blog(blog_post):
    """Validation to check blog contains title and author"""
    if not blog_post.get('title'):
        raise Exception("Title missing")
    if not blog_post.get('content'):
        raise Exception("Content missing")
    return True


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        #get the data from post request
        blog_post = request.get_json()

        # Validate the new post
        try:
            validate_blog(blog_post)
        except Exception as error:
            return jsonify({"error": str(error)}), 400

        #Create new id
        new_id = max([post['id'] for post in POSTS]) + 10
        blog_post['id'] = new_id

        # Add post to blogs list
        POSTS.append(blog_post)
        return jsonify(blog_post), 201
    else:
        # Handle Get request
        return jsonify(POSTS)

"""
@app.route('/api/posts/<post_id>', methods =['DELETE'])
def delete_post(post_id):
  """


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

"""
{
    "title": "<title of the new post>",
    "content": "<content of the new post>"
}
"""