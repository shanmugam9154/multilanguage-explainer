from flask import Blueprint, request, jsonify
from services.gemini_service import GeminiService

# Initialize Blueprint and Service
api_bp = Blueprint('api', __name__)
gemini_service = GeminiService()

def validate_payload(data, required_fields):
    """Helper to check for missing fields in request body."""
    missing = [field for field in required_fields if not data or field not in data]
    if missing:
        return False, f"Missing required fields: {', '.join(missing)}"
    return True, None

@api_bp.route('/explain', methods=['POST'])
def explain():
    """Endpoint to get a grade-level explanation of a topic."""
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_payload(data, ['topic', 'language', 'grade'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    # Call AI Service
    result = gemini_service.explain_topic(
        topic=data['topic'],
        language=data['language'],
        grade=data['grade']
    )
    
    status_code = 200 if "error" not in result else 500
    return jsonify(result), status_code

@api_bp.route('/summary', methods=['POST'])
def summary():
    """Endpoint to summarize provided text."""
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_payload(data, ['text', 'language'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    # Call AI Service
    result = gemini_service.summarize_text(
        text=data['text'],
        language=data['language']
    )
    
    status_code = 200 if "error" not in result else 500
    return jsonify(result), status_code

@api_bp.route('/quiz', methods=['POST'])
def quiz():
    """Endpoint to generate a 5-question MCQ quiz."""
    data = request.get_json()
    
    # Validation
    is_valid, error_msg = validate_payload(data, ['topic', 'language'])
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    # Call AI Service
    result = gemini_service.generate_quiz(
        topic=data['topic'],
        language=data['language']
    )
    
    status_code = 200 if "error" not in result else 500
    return jsonify(result), status_code

@api_bp.app_errorhandler(405)
def method_not_allowed(e):
    return jsonify({"error": "Method not allowed. Use POST."}), 405

@api_bp.app_errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Invalid JSON or bad request."}), 400