# Docker Deployment Guide for Discord Bot

## What's Been Set Up

This project is now configured to use Docker instead of Nixpacks, which should resolve the deployment issues you were experiencing with Coolify.

### Files Created

1. **`Dockerfile`** - Defines how to build and run your Discord bot in a container
2. **`.dockerignore`** - Excludes unnecessary files from the Docker build
3. **`nixpacks.toml`** - Can be deleted or kept (Docker takes precedence)

## Deploying to Coolify

### Step 1: Update Build Pack Settings

In your Coolify application dashboard:

1. Go to your application settings
2. Find **"Build Pack"** or **"Builder"** section
3. Change from **"Nixpacks"** to **"Dockerfile"**
4. Save the settings

### Step 2: Environment Variables

Make sure these environment variables are set in Coolify:

- `DISCORD_TOKEN` - Your Discord bot token
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase API key
- Any other variables from your `.env` file

### Step 3: Deploy

1. Commit and push the new Docker files to your repository:
   ```bash
   git add Dockerfile .dockerignore
   git commit -m "Add Docker support for deployment"
   git push
   ```

2. In Coolify, trigger a new deployment
3. The build should now succeed using the Dockerfile!

## Local Testing (Optional)

If you have Docker installed locally, you can test the build:

```bash
# Build the image
docker build -t dbot .

# Run the container (with environment variables)
docker run --env-file .env dbot
```

## Troubleshooting

### If deployment still fails:

1. Check Coolify logs for specific error messages
2. Verify all environment variables are set correctly
3. Make sure the repository is properly connected
4. Ensure Coolify has pulled the latest changes with the Dockerfile

### Common Issues:

- **Missing environment variables**: Add them in Coolify's environment section
- **Build timeout**: The first build might take longer; subsequent builds will be faster due to caching
- **Port configuration**: Discord bots don't need ports, but if Coolify requires one, you can ignore it or set it to any value

## What Changed from Nixpacks

- **More reliable**: Docker provides explicit, reproducible builds
- **Better caching**: Dependencies are cached between builds
- **Easier debugging**: Standard Docker commands work everywhere
- **No JSON config issues**: No more mysterious `thegameplan.json` errors!

## Need Help?

If you encounter any issues, check:
1. Coolify build logs
2. Container runtime logs
3. Environment variable configuration
