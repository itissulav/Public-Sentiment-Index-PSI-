# app/controllers/main_controller.py

from flask import Blueprint, render_template, session, flash, redirect, url_for, current_app, request, jsonify
import os
import json
from app.models.users import User
from app.services.supabase_client import admin_supabase
from app.utils.visualizer import ElectionDataVisualizer
from app.services import admin_service

# This MUST match what you import in __init__.py
main_bp = Blueprint("main", __name__)  

@main_bp.route("/")
def home():
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    return render_template("home.html", user=user)

@main_bp.route("/about")
def about():
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    return render_template("about.html", user=user)

@main_bp.route("/admin")
def admindashboard():
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    
    if not user:
        flash("You must be logged in to view that page.")
        return redirect(url_for("auth.login"))
        
    if str(user.get_role()).lower() != "admin":
        flash("Access Denied. Administrator privileges required.")
        return redirect(url_for("main.home"))
    
    total_users, all_users = admin_service.get_all_users()
    total_topics, all_topics = admin_service.get_all_topics()

    return render_template("admindashboard.html", user=user, total_users=total_users, all_users=all_users, total_topics=total_topics, topics=all_topics)

@main_bp.route("/trends", methods=["GET", "POST"])
def trends():
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    
    # Default CSV
    csv_filename = 'nepali_election.csv'
    current_topic = 'nepali_election'
    
    if request.method == "POST":
        topic_query = request.form.get("topic")
        if topic_query:
            from app.utils.fetcher import get_reddit_comments
            # Fetch data using the query
            get_reddit_comments(topic_query, limit_posts=100, subreddit_name="all", topic_name=topic_query)
            csv_filename = f"{topic_query}.csv"
            current_topic = topic_query

    # Path to CSV
    csv_path = os.path.join(current_app.root_path, 'static', 'analysed', csv_filename)
    
    if not os.path.exists(csv_path):
        flash(f"No data found for topic: {current_topic}")
        charts_data = {}
    else:
        try:
            # Initialize visualizer and get charts data
            vis = ElectionDataVisualizer(csv_path)
            charts_data = vis.get_all_charts_data()
        except Exception as e:
            flash(f"Error visualizing data: {str(e)}")
            charts_data = {}
    
    # Pass data to template as JSON dump to easily use in JS
    return render_template("trends.html", user=user, charts_data=json.dumps(charts_data), current_topic=current_topic)


# --- PROGRESS API ROUTE ---
@main_bp.route("/api/fetch_progress")
def get_fetch_progress():
    from app.utils.fetcher import fetch_progress
    return jsonify(fetch_progress)

# --- ADMIN API ROUTES FOR TOPICS ---

@main_bp.route("/admin/api/topics", methods=["POST"])
def api_add_topic():
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    if not user or str(user.get_role()).lower() != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    result = admin_service.add_topic(data)
    if result:
        return jsonify({"success": True, "data": result}), 201
    return jsonify({"error": "Failed to add topic"}), 500

@main_bp.route("/admin/api/topics/<int:topic_id>", methods=["PUT"])
def api_update_topic(topic_id):
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    if not user or str(user.get_role()).lower() != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    data = request.json
    result = admin_service.update_topic(topic_id, data)
    if result:
        return jsonify({"success": True, "data": result}), 200
    return jsonify({"error": "Failed to update topic"}), 500

@main_bp.route("/admin/api/topics/<int:topic_id>", methods=["DELETE"])
def api_delete_topic(topic_id):
    user_data = session.get("user")
    user = User.from_dict(user_data) if user_data else None
    if not user or str(user.get_role()).lower() != "admin":
        return jsonify({"error": "Unauthorized"}), 403
        
    success = admin_service.delete_topic(topic_id)
    if success:
        return jsonify({"success": True}), 200
    return jsonify({"error": "Failed to delete topic"}), 500
