import json
import logging
from django.http import JsonResponse
from django.shortcuts import render
import pandas as pd
from app.models import Data_Shift, angle_stored, Parameter_Settings, paraTableData

# Setting up logging
logger = logging.getLogger(__name__)

def report(request):
    if request.method == 'POST':
        try:
            raw_data = request.POST.get('data')
            if raw_data:
                data = json.loads(raw_data)

                from_date = data.get('from_date')
                part_model = data.get('part_model')
                to_date = data.get('to_date')
                shift = data.get('shift')

                # Check if required fields are present
                if not all([from_date, to_date, part_model]):
                    return JsonResponse({'error': 'Missing required fields: from_date, to_date, or part_model'}, status=400)

                # Prepare filter arguments
                filter_kwargs = {
                    'date__range': (from_date, to_date),
                    'part_model': part_model,
                }

                if shift != "ALL":
                    filter_kwargs['shift'] = shift

                # Fetch filtered data from the database
                filtered_data = angle_stored.objects.filter(**filter_kwargs).order_by('date')

                # Initialize the data dictionary for the table
                data_dict = {
                    'Date': [],
                    'Job Numbers': [],
                    'Shift': [],
                    'Operator': [],
                    'Angle': [],
                }

                # Get parameter data dynamically based on the part_model
                parameter_data = paraTableData.objects.filter(
                    parameter_settings__part_model=part_model
                ).values('parameter_name')

                # Add parameter name columns to the dictionary
                for param in parameter_data:
                    param_name = param['parameter_name']
                    data_dict[param_name] = []

                # Group data by Date and process each record
                grouped_data = {}
                unique_dates = set()

                for record in filtered_data:
                    date = record.date.strftime('%d-%m-%Y %I:%M:%S %p')
                    unique_dates.add(date)

                    # Create group for each date if not already present
                    if date not in grouped_data:
                        grouped_data[date] = {
                            'Job Numbers': set(),
                            'Shift': record.shift,
                            'Operator': record.operator,
                            'Angle': record.angleValue,
                            'Parameters': {param['parameter_name']: set() for param in parameter_data},
                        }

                    # Collect unique job numbers
                    if record.comp_sr_no:
                        grouped_data[date]['Job Numbers'].add(record.comp_sr_no)

                    # Add parameter readings for each record
                    for param in parameter_data:
                        param_name = param['parameter_name']
                        parameter_values = angle_stored.objects.filter(
                            comp_sr_no=record.comp_sr_no,
                            date=record.date,
                            parameter_name=param_name
                        ).values('output')

                        for pv in parameter_values:
                            grouped_data[date]['Parameters'][param_name].add(pv['output'])

                # Prepare the data dictionary for the DataFrame
                for date, group in grouped_data.items():
                    data_dict['Date'].append(date)

                    # Combine job numbers as a single string for display
                    job_numbers_combined = "<br>".join(sorted(group['Job Numbers'])) if group['Job Numbers'] else ''
                    data_dict['Job Numbers'].append(job_numbers_combined)

                    # Append values or empty string if not present
                    data_dict['Shift'].append(group['Shift'] if group['Shift'] else '')
                    data_dict['Operator'].append(group['Operator'] if group['Operator'] else '')
                    data_dict['Angle'].append(group['Angle'] if group['Angle'] else '')

                    # Add parameter readings to the data dictionary
                    for param in parameter_data:
                        param_name = param['parameter_name']
                        param_values = group['Parameters'][param_name]
                        
                        # Convert each value to string before joining
                        param_values_str = sorted(str(value) for value in param_values)
                        data_dict[param_name].append("<br>".join(param_values_str) if param_values_str else '')

                # Create a DataFrame from the data dictionary
                df = pd.DataFrame(data_dict)
                df.index = df.index + 1  # Adjust index to start from 1

                # Convert DataFrame to HTML
                table_html = df.to_html(index=True, escape=False, classes='table table-striped')

                return JsonResponse({
                    'table_html': table_html,
                    'total_count': len(unique_dates),
                })

        except Exception as e:
            # Log the exception
            logger.error("Error processing the report request", exc_info=True)
            return JsonResponse({'error': str(e)}, status=500)


    elif request.method == 'GET':
        shift_values = Data_Shift.objects.order_by('id').values_list('shift', 'shift_time').distinct()
        shift_name_queryset = Data_Shift.objects.order_by('id').values_list('shift', flat=True).distinct()
        shift_name = list(shift_name_queryset)

        # Convert the QuerySet to a list of lists
        shift_values_list = list(shift_values)
        
        # Serialize the list to JSON
        shift_values_json = json.dumps(shift_values_list)

        # Create context for the template
        context = {
            'shift_values': shift_values_json,
            'shift_name': shift_name,
        }

        return render(request, 'app/report.html', context)
