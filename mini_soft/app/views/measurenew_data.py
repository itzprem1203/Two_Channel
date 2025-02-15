from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import pytz
from app.models import angle_stored  # Import your model
from django.contrib.auth import authenticate

@csrf_exempt  # Disable CSRF for simplicity (only use in development or with proper safeguards)
def measurenew_data(request):
    if request.method == 'POST':

        
        try:
            data = json.loads(request.body)
            print("The value which is received from the frontend:", data)

            # Example of processing the data
            for entry in data:
                # Extract the date string from the request
                date_str = entry.get('date')  # Assuming 'date' is a string in 'dd/mm/yyyy hh:mm:ss AM/PM' format
                print("Original date string:", date_str)

                # Convert the date string to a datetime object
                try:
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y %I:%M:%S %p')

                    # Make the datetime object timezone-aware
                    timezone = pytz.timezone('Asia/Kolkata')  # Replace with your desired timezone
                    date_obj_aware = timezone.localize(date_obj)

                    # Optionally, you can convert the datetime object to UTC or remove timezone info if needed
                    date_obj_naive = date_obj_aware.replace(tzinfo=None)

                    print("Timezone-aware date:", date_obj_aware)
                    print("Naive date (without timezone):", date_obj_naive)

                except ValueError as e:
                    return JsonResponse({'status': 'error', 'message': f"Invalid date format: {str(e)}"}, status=400)

                # Now proceed to extract and store other fields
                comp_sr_no = entry.get('punchNo')
                print("comp_sr_no",comp_sr_no)
                part_model = entry.get('partModel')
                part_name = entry.get('partName')
                operator = entry.get('operator')
                shift = entry.get('shift')
                parameter_name = entry.get('parameterName')
                nominal = entry.get('nominal')
                output = entry.get('output')
                angleValue = entry.get('angleValue')
                andjacentValue = entry.get('andjacentValue')
                channelValue = entry.get('channelValue')


                # Create a new MeasurementData object and save it to the database
                measurement_data = angle_stored(
                    date=date_obj_naive,
                    comp_sr_no=comp_sr_no,
                    part_model=part_model,
                    part_name=part_name,
                    operator=operator,
                    shift=shift,
                    parameter_name=parameter_name,
                    nominal=nominal,
                    output=output,
                    angleValue = angleValue,
                    andjacentValue = andjacentValue,
                    channelValue = channelValue

                )

                # Save the measurement data to the database
                measurement_data.save()

            return JsonResponse({'status': 'success', 'message': 'Data received and saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)
