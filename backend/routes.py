# backend/routes.py
from flask import Blueprint, request, jsonify
from models import overlays_collection
from bson.objectid import ObjectId
from flasgger import swag_from

overlay_routes = Blueprint('overlays', __name__)

# Create Overlay
@overlay_routes.route('/', methods=['POST'])
@swag_from({
    'tags': ['Overlays'],
    'description': 'Create a new overlay',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string', 'enum': ['text', 'image']},
                    'content': {'type': 'string'},
                    'position': {
                        'type': 'object',
                        'properties': {
                            'x': {'type': 'integer'},
                            'y': {'type': 'integer'}
                        },
                        'required': ['x', 'y']
                    },
                    'size': {
                        'type': 'object',
                        'properties': {
                            'width': {'type': 'integer'},
                            'height': {'type': 'integer'}
                        },
                        'required': ['width', 'height']
                    }
                },
                'required': ['type', 'content', 'position', 'size']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Overlay created',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Bad Request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def create_overlay():
    data = request.get_json()
    # Validate required fields
    required_fields = ['type', 'content', 'position', 'size']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'{field} is required'}), 400
    result = overlays_collection.insert_one(data)
    return jsonify({'id': str(result.inserted_id)}), 201

# Read All Overlays
@overlay_routes.route('/', methods=['GET'])
@swag_from({
    'tags': ['Overlays'],
    'description': 'Retrieve all overlays',
    'responses': {
        200: {
            'description': 'A list of overlays',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'id': {'type': 'string'},
                        'type': {'type': 'string'},
                        'content': {'type': 'string'},
                        'position': {
                            'type': 'object',
                            'properties': {
                                'x': {'type': 'integer'},
                                'y': {'type': 'integer'}
                            }
                        },
                        'size': {
                            'type': 'object',
                            'properties': {
                                'width': {'type': 'integer'},
                                'height': {'type': 'integer'}
                            }
                        }
                    }
                }
            }
        }
    }
})
def get_overlays():
    overlays = []
    for overlay in overlays_collection.find():
        overlay['_id'] = str(overlay['_id'])
        overlay['id'] = overlay.pop('_id')  # Rename _id to id
        overlays.append(overlay)
    return jsonify(overlays), 200

# Read Single Overlay
@overlay_routes.route('/<id>', methods=['GET'])
@swag_from({
    'tags': ['Overlays'],
    'description': 'Retrieve a single overlay by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Overlay ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Overlay data',
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string'},
                    'type': {'type': 'string'},
                    'content': {'type': 'string'},
                    'position': {
                        'type': 'object',
                        'properties': {
                            'x': {'type': 'integer'},
                            'y': {'type': 'integer'}
                        }
                    },
                    'size': {
                        'type': 'object',
                        'properties': {
                            'width': {'type': 'integer'},
                            'height': {'type': 'integer'}
                        }
                    }
                }
            }
        },
        404: {
            'description': 'Overlay not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid ID format',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def get_overlay(id):
    try:
        overlay = overlays_collection.find_one({'_id': ObjectId(id)})
        if overlay:
            overlay['_id'] = str(overlay['_id'])
            overlay['id'] = overlay.pop('_id')  # Rename _id to id
            return jsonify(overlay), 200
        return jsonify({'error': 'Overlay not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

# Update Overlay
@overlay_routes.route('/<id>', methods=['PUT'])
@swag_from({
    'tags': ['Overlays'],
    'description': 'Update an existing overlay by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Overlay ID'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'type': {'type': 'string', 'enum': ['text', 'image']},
                    'content': {'type': 'string'},
                    'position': {
                        'type': 'object',
                        'properties': {
                            'x': {'type': 'integer'},
                            'y': {'type': 'integer'}
                        }
                    },
                    'size': {
                        'type': 'object',
                        'properties': {
                            'width': {'type': 'integer'},
                            'height': {'type': 'integer'}
                        }
                    }
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Overlay updated',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Overlay not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid ID format',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def update_overlay(id):
    data = request.get_json()
    try:
        result = overlays_collection.update_one({'_id': ObjectId(id)}, {'$set': data})
        if result.matched_count:
            return jsonify({'message': 'Overlay updated'}), 200
        return jsonify({'error': 'Overlay not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400

# Delete Overlay
@overlay_routes.route('/<id>', methods=['DELETE'])
@swag_from({
    'tags': ['Overlays'],
    'description': 'Delete an overlay by ID',
    'parameters': [
        {
            'name': 'id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'Overlay ID'
        }
    ],
    'responses': {
        200: {
            'description': 'Overlay deleted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'}
                }
            }
        },
        404: {
            'description': 'Overlay not found',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid ID format',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def delete_overlay(id):
    try:
        result = overlays_collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count:
            return jsonify({'message': 'Overlay deleted'}), 200
        return jsonify({'error': 'Overlay not found'}), 404
    except:
        return jsonify({'error': 'Invalid ID format'}), 400
