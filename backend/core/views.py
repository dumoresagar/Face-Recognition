from django.shortcuts import render
from django.views.generic import TemplateView


class HomePageView(TemplateView):

    template_name = 'index.html'



# import os

# def dynamic_upload_path(instance, filename):
#     # Extract the district, taluka, and village codes from the filename
#     district_code = filename[:3]
#     taluka_code = filename[3:7]
#     village_code = filename[7:13]
#     print("Distrct Code",district_code)
#     print("Taluka Code",taluka_code)
#     print("Village Code",village_code)
    
#     district_name = District.objects.filter(district_code=district_code).values('district_name')
#     print("AAAAAAAAAAAAAAAAAa",district_name)

#     taluka_name = Taluka.objects.filter(taluka_code=district_code).values('taluka_name')
#     print("BBBBBBBBBBBBBBBB",taluka_name)

#     village_name = Village.objects.filter(village_code=district_code).values('village_name')
#     print("CCCCCCCCCCCCCCC",village_name)



#     # Define the base directory where uploads will be stored
#     base_dir = 'uploads'

#     # Create the full directory path based on the codes
#     district_dir = os.path.join(base_dir, district_name)
#     taluka_dir = os.path.join(district_dir, taluka_name)
#     village_dir = os.path.join(taluka_dir, village_name)

#     # Create the directories if they don't exist
#     for directory in [base_dir, district_dir, taluka_dir, village_dir]:
#         if not os.path.exists(directory):
#             os.makedirs(directory)

#     # Return the final path for the uploaded file
#     return os.path.join(village_dir, filename)