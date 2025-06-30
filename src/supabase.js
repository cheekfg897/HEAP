import { createClient } from '@supabase/supabase-js'

<<<<<<< Updated upstream
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

=======

// 1. Get the environment variables from your .env.local file.
//    import.meta.env is a Vite-specific feature that exposes env variables.
const supabaseUrl = "https://culnykmmgfetgpuglvrt.supabase.co"
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN1bG55a21tZ2ZldGdwdWdsdnJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NTgwMzcsImV4cCI6MjA2NTIzNDAzN30.q2eGpMlEkhAj32na-U7No_7ffNGv_HgECLpn1GCLyR0"

// 2. Create the Supabase client.
//    This object will be your single point of interaction with Supabase services.
//    We use 'export' to make this instance available to other files in our project.
>>>>>>> Stashed changes
export const supabase = createClient(supabaseUrl, supabaseAnonKey)