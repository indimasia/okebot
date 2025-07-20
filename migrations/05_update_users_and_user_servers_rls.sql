-- Drop existing RLS policies for users table
drop policy if exists "Enable read access for all" on users;
drop policy if exists "Enable insert access for all" on users;
drop policy if exists "Enable update for all" on users;

-- Create new policies with service role bypass for users table
create policy "Enable read access for service role" on users
  for select
  using (true);

create policy "Enable insert for service role" on users
  for insert
  with check (true);

create policy "Enable update for service role" on users
  for update
  using (true);

-- Grant necessary permissions to service role for users table
grant all on users to service_role;

-- Drop existing RLS policies for user_servers table
drop policy if exists "Enable read access for all" on user_servers;
drop policy if exists "Enable insert access for all" on user_servers;
drop policy if exists "Enable update for all" on user_servers;

-- Create new policies with service role bypass for user_servers table
create policy "Enable read access for service role" on user_servers
  for select
  using (true);

create policy "Enable insert for service role" on user_servers
  for insert
  with check (true);

create policy "Enable update for service role" on user_servers
  for update
  using (true);

-- Grant necessary permissions to service role for user_servers table
grant all on user_servers to service_role;