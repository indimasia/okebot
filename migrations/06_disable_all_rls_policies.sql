-- Migration: Disable all RLS policies and make all tables open
-- This migration removes all Row Level Security policies and disables RLS on all tables
-- making them completely open for all operations without any restrictions

-- Drop all existing RLS policies for users table
drop policy if exists "Enable read access for service role" on users;
drop policy if exists "Enable insert for service role" on users;
drop policy if exists "Enable update for service role" on users;
drop policy if exists "Enable delete for service role" on users;
drop policy if exists "Enable read access for all" on users;
drop policy if exists "Enable insert access for all" on users;
drop policy if exists "Enable update for all" on users;
drop policy if exists "Enable delete for all" on users;

-- Drop all existing RLS policies for servers table
drop policy if exists "Enable read access for service role" on servers;
drop policy if exists "Enable insert for service role" on servers;
drop policy if exists "Enable update for service role" on servers;
drop policy if exists "Enable delete for service role" on servers;
drop policy if exists "Enable read access for all" on servers;
drop policy if exists "Enable insert access for all" on servers;
drop policy if exists "Enable update for all" on servers;
drop policy if exists "Enable delete for all" on servers;

-- Drop all existing RLS policies for user_servers table
drop policy if exists "Enable read access for service role" on user_servers;
drop policy if exists "Enable insert for service role" on user_servers;
drop policy if exists "Enable update for service role" on user_servers;
drop policy if exists "Enable delete for service role" on user_servers;
drop policy if exists "Enable read access for all" on user_servers;
drop policy if exists "Enable insert access for all" on user_servers;
drop policy if exists "Enable update for all" on user_servers;
drop policy if exists "Enable delete for all" on user_servers;

-- Disable Row Level Security on all tables
alter table users disable row level security;
alter table servers disable row level security;
alter table user_servers disable row level security;

-- Grant full access to all roles (anon, authenticated, service_role)
grant all privileges on users to anon, authenticated, service_role;
grant all privileges on servers to anon, authenticated, service_role;
grant all privileges on user_servers to anon, authenticated, service_role;

-- Grant usage on sequences if they exist
grant usage, select on all sequences in schema public to anon, authenticated, service_role;

-- Ensure all future tables will also be accessible
alter default privileges in schema public grant all on tables to anon, authenticated, service_role;
alter default privileges in schema public grant usage, select on sequences to anon, authenticated, service_role;

-- Add comment for documentation
comment on table users is 'RLS disabled - open access for all operations';
comment on table servers is 'RLS disabled - open access for all operations';
comment on table user_servers is 'RLS disabled - open access for all operations';
