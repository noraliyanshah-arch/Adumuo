# Troubleshooting Guide - Admin Login

## Masalah: Tidak Boleh Log Masuk

### Langkah Penyelesaian:

1. **Pastikan Backend Server Berjalan**
   ```bash
   cd backend
   python main.py
   ```
   Server harus berjalan di `http://localhost:8000`

2. **Pastikan Dependencies Diinstall**
   ```bash
   pip install python-jose[cryptography] passlib[bcrypt]
   ```

3. **Test Login dengan Script**
   ```bash
   python test_admin_login.py
   ```

4. **Credentials Default**
   - Username: `admin`
   - Password: `admin123`

5. **Check Browser Console**
   - Buka Developer Tools (F12)
   - Lihat tab Console untuk error messages
   - Check tab Network untuk melihat request/response

6. **Common Issues:**
   - **CORS Error**: Pastikan backend CORS middleware mengizinkan origin frontend
   - **Connection Refused**: Backend tidak berjalan atau port salah
   - **401 Unauthorized**: Username/password salah
   - **500 Internal Server Error**: Check backend logs untuk detail error

7. **Ubah Credentials (Production)**
   Set environment variables:
   ```bash
   export ADMIN_USERNAME=your_username
   export ADMIN_PASSWORD=your_password
   ```


