-- Drop existing RLS policies for servers table
drop policy if exists "Enable read access for all" on servers;
drop policy if exists "Enable insert access for all" on servers;
drop policy if exists "Enable update for all" on servers;

-- Create new policies with service role bypass
create policy "Enable read access for service role" on servers
  for select
  using (true);

create policy "Enable insert for service role" on servers
  for insert
  with check (true);

create policy "Enable update for service role" on servers
  for update
  using (true);

-- Grant necessary permissions to service role
grant all on servers to service_role;