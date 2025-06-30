import { createClient } from '@supabase/supabase-js'

// These variables are automatically loaded from your .env file by Vite
// Ensure your .env file has these exact names:
// VITE_SUPABASE_URL="https://your-project-id.supabase.co"
// VITE_SUPABASE_ANON_KEY="your-public-anon-key"
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

if (!supabaseUrl || !supabaseAnonKey) {
  console.error("Supabase URL or Anon Key is missing. Check your .env file.");
  // You might want to throw an error or handle this more gracefully in a real app
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey)