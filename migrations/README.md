# Database Migrations

This directory contains SQL migration files for setting up and updating the database schema in Supabase.

## Migration Files

1. `01_create_users_table.sql`
   - Creates the users table to store Discord user information
   - Includes fields: id, discord_id, username, registered_at, avatar_url
   - Sets up initial RLS policies

2. `02_create_servers_table.sql`
   - Creates the servers table to store Discord server information
   - Includes fields: id, server_id, name, icon_url, member_count, created_at, owner_id
   - Sets up initial RLS policies

3. `03_create_user_servers_table.sql`
   - Creates the user_servers table for many-to-many relationships
   - Includes fields: id, user_id, server_id, joined_at, registered_by
   - Creates server_registration_stats view
   - Sets up initial RLS policies

4. `04_update_servers_rls.sql`
   - Updates Row Level Security policies for the servers table
   - Grants necessary permissions to service role
   - Ensures proper access for bot operations

5. `05_update_users_and_user_servers_rls.sql`
   - Updates Row Level Security policies for users and user_servers tables
   - Grants necessary permissions to service role
   - Ensures consistent access policies across all tables

## How to Apply Migrations

1. Open the Supabase Dashboard
2. Navigate to the SQL Editor
3. Apply migrations in order by copying and executing each SQL file
4. Verify the changes in the Table Editor

## Schema Overview

### Security
- Row Level Security (RLS) is enabled on all tables
- Service role has full access to all tables
- Policies are configured to allow necessary operations for the bot

### Indexing
- Indexes are created on frequently queried columns
- discord_id and server_id have unique constraints
- Foreign key relationships maintain data integrity

### Views
- server_registration_stats: Provides registration statistics per server