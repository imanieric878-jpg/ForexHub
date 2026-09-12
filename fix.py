import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove readdy project version and preview links
content = re.sub(r'<meta name="readdy-project-version" content="[^"]+">\n?', '', content)
content = re.sub(r'<script type="module" crossorigin src="/preview/[^"]+"></script>\n?', '', content)
content = re.sub(r'<link rel="stylesheet" crossorigin href="/preview/[^"]+">\n?', '', content)
content = re.sub(r'<link type="image/png" rel="icon" href="https://public.readdy.ai/gen_page/readdy-logo.png">\n?', '', content)
content = re.sub(r'<script src="https://cdn.jsdelivr.net/npm/posthog-js[^"]+" async></script>\n?', '', content)

# 2. Add tailwind CDN before </head> to preserve styling (since the original CSS is removed)
if "cdn.tailwindcss.com" not in content:
    tailwind_script = """<script src="https://cdn.tailwindcss.com"></script>
<script>
  tailwind.config = {
    theme: {
      extend: {
        colors: {
          primary: { 50: '#f0fdf4', 100: '#dcfce7', 200: '#bbf7d0', 300: '#86efac', 400: '#4ade80', 500: '#22c55e', 600: '#16a34a', 700: '#15803d', 800: '#166534', 900: '#14532d', 950: '#052e16' },
          secondary: { 50: '#fdf8f6', 100: '#f2e8e5', 200: '#eaddd7', 300: '#e0cec7', 400: '#d2bab0', 500: '#a18072', 600: '#977669', 700: '#846358', 800: '#43302b', 900: '#1c1411', 950: '#1c1411' },
          background: { 50: '#F6F6F6', 100: '#E7E7E7', 200: '#D1D1D1', 300: '#B0B0B0', 400: '#888888', 500: '#6D6D6D', 600: '#5D5D5D', 700: '#4F4F4F', 800: '#454545', 900: '#3D3D3D', 950: '#1F1F1F' },
          foreground: { 50: '#F5F5F5', 100: '#E9E9E9', 200: '#D9D9D9', 300: '#C4C4C4', 400: '#9D9D9D', 500: '#7B7B7B', 600: '#555555', 700: '#434343', 800: '#262626', 900: '#101010', 950: '#101010' },
          accent: { 50: '#faf5fd', 100: '#f3e8fa', 200: '#e9d5f4', 300: '#d8b4eb', 400: '#c286df', 500: '#a758ce', 600: '#8c3bab', 700: '#732e8c', 800: '#612874', 900: '#50235f', 950: '#310d3e' },
        },
        fontFamily: {
          heading: ['Sora', 'sans-serif'],
          mono: ['IBM Plex Mono', 'monospace'],
          'mono-label': ['IBM Plex Mono', 'monospace'],
        },
      }
    }
  }
</script>
</head>"""
    content = content.replace("</head>", tailwind_script)

# 3. Replace all readdy.ai search-image links with assets/bg.jpg
content = re.sub(r'src="https://readdy\.ai/api/search-image\?[^"]+"', 'src="assets/bg.jpg"', content)

# 4. Fix HTML structural errors
# Error 1: Stray </span>
err1 = '''          <span class="flex items-center gap-6 px-6 font-mono-label text-[11px] uppercase tracking-[0.22em] text-background-200/70 whitespace-nowrap">
            No guaranteed profits
            <span class="w-1 h-1 rounded-full bg-accent-500"></span>
          </span>
          </span>
        <span class="flex items-center gap-6 px-6 font-mono-label text-[11px] uppercase tracking-[0.22em] text-background-200/70 whitespace-nowrap">'''
fix1 = '''          <span class="flex items-center gap-6 px-6 font-mono-label text-[11px] uppercase tracking-[0.22em] text-background-200/70 whitespace-nowrap">
            No guaranteed profits
            <span class="w-1 h-1 rounded-full bg-accent-500"></span>
          </span>
        <span class="flex items-center gap-6 px-6 font-mono-label text-[11px] uppercase tracking-[0.22em] text-background-200/70 whitespace-nowrap">'''
content = content.replace(err1, fix1)

# Error 2: Missing div flex for youtube
err2 = '''              <a href="#" rel="nofollow" class="group rounded-lg border bg-background-50 p-5 transition-colors duration-200 cursor-pointer border-dashed border-background-300 hover:border-accent-400">
                <span class="w-11 h-11 flex items-center justify-center rounded-md text-xl transition-colors duration-200 bg-secondary-100 text-secondary-700 group-hover:bg-accent-100 group-hover:text-accent-700">
                    <i class="ri-youtube-line"></i>
                  </span>
                  <i class="ri-arrow-right-up-line text-foreground-400 transition-colors duration-200 group-hover:text-primary-600"></i>
                </div>'''
fix2 = '''              <a href="#" rel="nofollow" class="group rounded-lg border bg-background-50 p-5 transition-colors duration-200 cursor-pointer border-dashed border-background-300 hover:border-accent-400">
                <div class="flex items-center justify-between">
                  <span class="w-11 h-11 flex items-center justify-center rounded-md text-xl transition-colors duration-200 bg-secondary-100 text-secondary-700 group-hover:bg-accent-100 group-hover:text-accent-700">
                    <i class="ri-youtube-line"></i>
                  </span>
                  <i class="ri-arrow-right-up-line text-foreground-400 transition-colors duration-200 group-hover:text-primary-600"></i>
                </div>'''
content = content.replace(err2, fix2)

# Error 3: Stray </div> around line 256
err3 = '''                <h3 class="mt-4 font-heading text-sm md:text-base font-semibold text-foreground-950">Structured Decisions</h3>
                <p class="mt-1.5 text-xs md:text-sm leading-relaxed text-foreground-600">Knowing the reason behind a trade before any action is taken.</p>
              </div>
              </div>
              <div class="group rounded-lg border border-background-200 bg-background-100 p-5 transition-colors duration-200 hover:border-primary-300 hover:bg-background-50">'''
fix3 = '''                <h3 class="mt-4 font-heading text-sm md:text-base font-semibold text-foreground-950">Structured Decisions</h3>
                <p class="mt-1.5 text-xs md:text-sm leading-relaxed text-foreground-600">Knowing the reason behind a trade before any action is taken.</p>
              </div>
              <div class="group rounded-lg border border-background-200 bg-background-100 p-5 transition-colors duration-200 hover:border-primary-300 hover:bg-background-50">'''
content = content.replace(err3, fix3)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)
print("Done fixing index.html")
