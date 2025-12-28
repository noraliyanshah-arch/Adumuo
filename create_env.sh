#!/bin/bash

# Create .env file with Supabase connection string
cat > .env << 'EOF'
# Database Configuration
DATABASE_URL=postgresql://postgres:596AU7F5IPYSgnG3@db.havuplfcaltsphvdllof.supabase.co:5432/postgres

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Environment
ENVIRONMENT=development
EOF

echo "✅ .env file created successfully!"
echo "📝 Database URL configured for Supabase"


