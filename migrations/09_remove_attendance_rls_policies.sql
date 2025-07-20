-- Remove all RLS policies from attendance table
-- This migration disables RLS and drops all existing policies

-- Drop all existing policies on attendance table
drop policy if exists "Enable read access for authenticated users" on attendance;
drop policy if exists "Enable insert access for authenticated users" on attendance;
drop policy if exists "Enable update access for authenticated users" on attendance;

-- Disable RLS on attendance table
alter table attendance disable row level security;
