import os
import secrets
from PIL import Image
from flask import url_for, current_app                      # current_app will let us import the correct instance of app
from flask_mail import Message
from app import mail
from app.utils import url_for_secure
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

def isCloudSinarySetUp():
    return None not in [
        current_app.config['CLOUDINARY_CLOUD_NAME'], 
        current_app.config['CLOUDINARY_API_KEY'], 
        current_app.config['CLOUDINARY_API_SECRET']
    ]

def save_cloud(form_picture, image_res = (125, 125)):                                    
    upload_result = upload(form_picture)
    img_url, options = cloudinary_url(upload_result['public_id'], format="jpg", crop="fill", width=image_res[0], height=image_res[1], secure=True) 
    return img_url

def save_static(form_picture, image_res = (125, 125)):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)                                      # The underscore _ represent's an unused variable we don't need. The split ext, is similar to Python's split function, in that it splits a string where the '.' extension appears. 
    picture_fn = random_hex + f_ext                                                         # By concatenating them we are now able to get uniquely hashed image names, but they can still have the correct extenstion
    picture_path = os.path.join(current_app.root_path, 'static/profile_images', picture_fn )         
    
    output_res = image_res                                                               # The output resolution is a tuple set to (125x125) pixels.
    with Image.open(form_picture) as i:                                                          # We are opening the original image 'form_picture' in order to generate a copy image 'i' which will be downscaled into a specified resolution.
        i.thumbnail(output_res)                                                                 # Thumbnail is part of Image and PIL, or Pillow which is a python package that resizes images to the specified resolution. 'i' has now been rescaled to (125x125) px.
        i.save(picture_path)                                                                    # We are saving 'i' instead of form_picture locally, because of space efficiency. It would make no sense to save a 4k image only for it to be scaled down in CSS. Inefficient in db storage and load times!
    return url_for_secure('static', filename='profile_images/' + picture_fn)

def save_picture(form_picture):
    if isCloudSinarySetUp():
        try:
            return save_cloud(form_picture, image_res=(125, 125))
        except:
            print('Invalid cloud storage settings, using static storage instead')
    return save_static(form_picture, image_res=(125, 125))




# Note to self inorder to use f strings you need to make sure you have Python 3.6 or greater!
# When using multi line f strings 
# ''' { you only need 1 set of braces to insert python code, rather than {{ 2 }} like you would normally in jinja2 syntax! } ''' 
# Another thing to note is that Indentation will be carried over into the text, and we don't want that! 
# Setting _external to true allows us to use absolute URL's not just relative URL's that would work on localhost but not on deployemnt level!

def send_reset_email(user):                 # Helper Function to send reset email!
    token = user.get_reset_token()          # For now we're sticking to the defaults!
    msg = Message(  subject='Password Reset Request', 
                    sender='noreply@codehub.demo.com', 
                    recipients=[user.email] )
    msg.body = f'''To reset your password, please visit the following link: 
{url_for_secure('users.reset_token', token=token, _external=True) }

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)                          # This is sending the message using mail.send()


