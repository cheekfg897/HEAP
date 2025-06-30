import { createClient } from '@supabase/supabase-js'


// 1. Get the environment variables from your .env.local file.
//    import.meta.env is a Vite-specific feature that exposes env variables.
const supabaseUrl = "https://culnykmmgfetgpuglvrt.supabase.co"
const supabaseAnonKey = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN1bG55a21tZ2ZldGdwdWdsdnJ0Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NDk2NTgwMzcsImV4cCI6MjA2NTIzNDAzN30.q2eGpMlEkhAj32na-U7No_7ffNGv_HgECLpn1GCLyR0"

// 2. Create the Supabase client.
//    This object will be your single point of interaction with Supabase services.
//    We use 'export' to make this instance available to other files in our project.
export const supabase = createClient(supabaseUrl, supabaseAnonKey)