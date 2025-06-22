// src/supabase.js
import { createClient } from '@supabase/supabase-js'

// Load environment variables. In a Vue CLI project, these usually start with VUE_APP_
// In a Vite project (Vue 3 setup), they typically start with VITE_
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || 'SUPABASE_URL';
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || 'SUPABASE_ANON_KEY';

// Make sure your environment variables are actually set!
if (!supabaseUrl || !supabaseAnonKey) {
  console.error('Supabase URL or Anon Key is not set. Please check your environment variables.');
}

export const supabase = createClient(supabaseUrl, supabaseAnonKey);