# Frontend Setup

## Background Image

The landing page uses a beautiful background image. To use a custom Muar image:

1. Place your image in the `frontend/images/` directory
2. Update the `background-image` URL in `index.html` (line ~30) to point to your image:
   ```css
   background-image: url('images/muar-background.jpg');
   ```

Alternatively, you can use any image URL from the web.

## Language Support

The site supports both Malay (MS) and English (EN). The language preference is saved in localStorage and persists across sessions.

## Image Upload

Users can either:
- Upload an image file directly from their device
- Enter an image URL

Uploaded images are saved to the `backend/uploads/` directory.

## Admin Access

Default admin credentials:
- Username: `admin`
- Password: `admin123`

**Important:** Change these credentials in production by setting environment variables:
- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`


