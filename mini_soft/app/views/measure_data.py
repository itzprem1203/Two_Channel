from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import pytz
from app.models import angle_stored  # Import your model
from django.contrib.auth import authenticate


@csrf_exempt
def delete_measure_data(request):
    if request.method == 'POST':
        try:
            # Parse JSON data from request body
            data = json.loads(request.body)

            comp_sr_no = data.get('input_value', '')  # Get comp_sr_no
            part_model = data.get('part_model', '')  # Get part_model
            user_id = data.get('user_id', '')  # Get user ID (from credentials request)
            password = data.get('password', '')  # Get password (from credentials request)

            # Step 1: Check if comp_sr_no exists for the specified part_model
            existing_record = angle_stored.objects.filter(comp_sr_no=comp_sr_no, part_model=part_model)

            if existing_record.exists():
                # Step 2: Send response for overwrite confirmation if the record exists
                if not user_id or not password:  # Credentials not provided yet
                    return JsonResponse({
                        'status': 'exists',
                        'message': f'Punch number "{comp_sr_no}" already exists for model "{part_model}". Do you want to overwrite it?'
                    })

                # Step 3: If credentials are provided, verify them and proceed with deletion
                if user_id != 'admin' or password != 'admin':
                    return JsonResponse({'success': False, 'message': 'Invalid credentials!'})

                # Proceed with deletion
                deleted_count, _ = existing_record.delete()

                if deleted_count > 0:
                    return JsonResponse({'success': True, 'message': 'Punch number deleted successfully!'})
                else:
                    return JsonResponse({'success': False, 'message': 'Punch number not found for this model!'})

            else:
                # If comp_sr_no doesn't exist, simply return a success response without triggering the overwrite flow
                return JsonResponse({'success': True, 'message': 'New punch number, no action needed for deletion.'})

        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})

    return JsonResponse({'success': False, 'message': 'Invalid request'})