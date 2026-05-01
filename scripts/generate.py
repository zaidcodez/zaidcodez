import os
import requests
import random

TOKEN = os.environ["ACCESS_TOKEN"]
USER = os.environ["USER_NAME"]

HEADERS = {"Authorization": f"token {TOKEN}"}


def get_stats():
    query = """
    query($login: String!) {
      user(login: $login) {
        contributionsCollection {
          totalCommitContributions
        }
        repositories {
          totalCount
        }
        followers {
          totalCount
        }
        starredRepositories {
          totalCount
        }
      }
    }
    """

    r = requests.post(
        "https://api.github.com/graphql",
        json={"query": query, "variables": {"login": USER}},
        headers=HEADERS
    )

    data = r.json()["data"]["user"]

    return {
        "commits": data["contributionsCollection"]["totalCommitContributions"],
        "repos": data["repositories"]["totalCount"],
        "followers": data["followers"]["totalCount"],
        "stars": data["starredRepositories"]["totalCount"]
    }


def build_svg(s):

    import random

    logs = [
        "fetch_user --github",
        "parse_repositories --all",
        "collect_commit_matrix",
        "resolve_social_links",
        "mount_profile_index"
    ]

    log_line = random.choice(logs)

    return f"""
<svg width="1000" height="600" xmlns="http://www.w3.org/2000/svg">
<g clip-path="url(#screen)">

  <defs>

    <pattern id="scan" width="1000" height="4" patternUnits="userSpaceOnUse">
      <rect width="1000" height="2" fill="#7FAFC2" opacity="0.035"/>
    </pattern>

    <filter id="noise">
      <feTurbulence type="fractalNoise"
                    baseFrequency="0.75"
                    numOctaves="2"
                    stitchTiles="stitch"/>
      <feColorMatrix type="matrix"
        values="
          1 0 0 0 0
          0 1 0 0 0
          0 0 1 0 0
          0 0 0 0.04 0"/>
    </filter>

    <filter id="glow">
      <feGaussianBlur stdDeviation="1.6" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>

    <filter id="jitter">
      <feTurbulence type="fractalNoise" baseFrequency="0.012" numOctaves="1" seed="3" result="n"/>
      <feDisplacementMap in="SourceGraphic" in2="n" scale="1.2"/>
    </filter>
    
    <!-- MONITOR SCREEN CLIP -->
    <clipPath id="screen">
      <rect x="25" y="25" width="950" height="550" rx="28"/>
    </clipPath>

    <!-- CLIP PATHS (typing effect) -->
    <clipPath id="clip1"><rect x="70" y="170" width="0" height="25"><animate attributeName="width" from="0" to="320" dur="0.5s" begin="0s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip2"><rect x="70" y="200" width="0" height="25"><animate attributeName="width" from="0" to="430" dur="0.6s" begin="0.5s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip3"><rect x="70" y="230" width="0" height="25"><animate attributeName="width" from="0" to="620" dur="0.8s" begin="1.1s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip4"><rect x="70" y="260" width="0" height="25"><animate attributeName="width" from="0" to="620" dur="0.8s" begin="1.8s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip5"><rect x="70" y="290" width="0" height="25"><animate attributeName="width" from="0" to="520" dur="0.8s" begin="2.5s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip6"><rect x="70" y="320" width="0" height="25"><animate attributeName="width" from="0" to="560" dur="0.8s" begin="3.2s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip7"><rect x="70" y="350" width="0" height="25"><animate attributeName="width" from="0" to="430" dur="0.7s" begin="3.9s" fill="freeze"/></rect></clipPath>
    <clipPath id="clip8"><rect x="70" y="395" width="0" height="25"><animate attributeName="width" from="0" to="340" dur="0.6s" begin="4.6s" fill="freeze"/></rect></clipPath>

  </defs>

  <!-- BG -->
  
  <!-- MONITOR BODY -->
<rect x="10" y="10" width="980" height="580" rx="35"
      fill="#020409"
      stroke="#7FAFC2"
      stroke-opacity="0.15"
      stroke-width="2"/>

      <!-- SCREEN AREA -->
<rect x="25" y="25" width="950" height="550" rx="28"
      fill="#05070b"/>

  <rect width="1000" height="600" fill="url(#scan)"/>

  <!-- TOP BAR -->
  <rect x="40" y="30" width="920" height="70" rx="12"
        fill="#0a0f14" stroke="#7FAFC2" stroke-opacity="0.14"/>

  <text x="70" y="75" fill="#7FAFC2" font-family="monospace" font-size="22" filter="url(#glow)">
    CONTROL PANEL
  </text>
  <text x="820" y="75"
        fill="#7FAFC2"
        font-family="monospace"
        font-size="13"
        opacity="0">
    STATUS : ONLINE
    <animate attributeName="opacity" from="0" to="1" dur="0.3s" begin="5.5s" fill="freeze"/>
  </text>

  <!-- ACCESS FLASH -->
  <text x="380" y="95"
        fill="#7FAFC2"
        font-family="monospace"
        font-size="12"
        opacity="0">
    ACCESS GRANTED
    <animate attributeName="opacity" values="0;0;0.7;0;0" dur="7s" repeatCount="indefinite"/>
  </text>

  <!-- LEFT PANEL -->
  <rect x="40" y="120" width="600" height="430" rx="12"
        fill="#0a0f14" stroke="#7FAFC2" stroke-opacity="0.08"
        filter="url(#jitter)"/>

  <text x="65" y="150" fill="#7FAFC2" font-family="monospace" font-size="13" opacity="0.45">
    root@zaidnode:~$
  </text>

  <!-- BOOT LINES -->
  <text x="70" y="185" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip1)">
    > ./init_kernel --profile
  </text>

  <text x="70" y="215" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip2)">
    > {log_line} ................[OK]
  </text>

  <text x="70" y="245" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip3)">
    > Email.work ............... zaid.ahmed.techwork@gmail.com
  </text>

  <text x="70" y="275" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip4)">
    > Email.personal ........... zaidahmedsheikh10@gmail.com
  </text>

  <text x="70" y="305" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip5)">
    > Languages.prog ........... JavaScript Python C++
  </text>

  <text x="70" y="335" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip6)">
    > Languages.web ............ HTML CSS MongoDB MySQL
  </text>

  <text x="70" y="365" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip7)">
    > LinkedIn.handle .......... zaidahmed10
  </text>

  <text x="70" y="410" fill="#7FAFC2" font-family="monospace" font-size="15" clip-path="url(#clip8)">
    > open_for_collabs = TRUE
  </text>

  <!-- BLINK CURSOR (fixed timing) -->
  <text x="280" y="410" fill="#7FAFC2" font-family="monospace" opacity="0">
    █
    <animate attributeName="opacity"
             from="0" to="1"
             dur="0.01s"
             begin="5.2s"
             fill="freeze"/>
    <animate attributeName="opacity"
             values="1;0;1"
             dur="0.7s"
             begin="5.25s"
             repeatCount="indefinite"/>
  </text>

  <!-- STATUS LINE -->
  <text x="70" y="480" fill="#7FAFC2" font-family="monospace" font-size="12" opacity="0">
    process://github_profile_render completed successfully
    <animate attributeName="opacity" from="0" to="0.45" dur="0.3s" begin="5.45s" fill="freeze"/>
  </text>

  <!-- DAEMON CHATTER -->
  <text x="70" y="510" fill="#7FAFC2" font-family="monospace" font-size="11" opacity="0">
    daemon://watcher listening on port 443
    <animate attributeName="opacity" from="0" to="0.35" dur="0.3s" begin="5.7s" fill="freeze"/>
    <animate attributeName="opacity" values="0.35;0.1;0.35" dur="1.5s" begin="6s" repeatCount="indefinite"/>
  </text>

  <text x="70" y="530" fill="#7FAFC2" font-family="monospace" font-size="11" opacity="0">
    memory allocation stable :: no faults detected
    <animate attributeName="opacity" from="0" to="0.2" dur="0.3s" begin="5.9s" fill="freeze"/>
    <animate attributeName="opacity" values="0.2;0.05;0.2" dur="2s" begin="6.2s" repeatCount="indefinite"/>
  </text>

  <!-- LIVE PROMPT -->
  <text x="70" y="570" fill="#7FAFC2" font-family="monospace" font-size="12" opacity="0">
    root@zaidnode:~$ _
    <animate attributeName="opacity" from="0" to="0.45" dur="0.3s" begin="6.8s" fill="freeze"/>
    <animate attributeName="opacity" values="0.45;0.18;0.45" dur="1s" begin="7s" repeatCount="indefinite"/>
  </text>

  <!-- RIGHT PANEL -->
<!-- RIGHT PANEL -->
<rect x="670" y="120" width="290" height="430" rx="12"
      fill="#0a0f14" stroke="#7FAFC2" stroke-opacity="0.08"
      opacity="0">
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.35s"
           begin="5.4s"
           fill="freeze"/>
</rect>

<!-- TITLE -->
<text x="700" y="170"
      fill="#7FAFC2"
      font-family="monospace"
      font-size="13"
      opacity="0">
  LIVE METRICS
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.3s"
           begin="5.55s"
           fill="freeze"/>
</text>

<!-- METRICS (COMMITS) -->
<text x="700" y="220"
      fill="#7FAFC2"
      font-family="monospace"
      opacity="0">
  COMMITS
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="5.7s"
           fill="freeze"/>
</text>

<text x="700" y="250"
      fill="#7FAFC2"
      font-family="monospace"
      font-size="24"
      opacity="0">
  {s['commits']}
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="5.8s"
           fill="freeze"/>
</text>

<!-- REPOS -->
<text x="700" y="300"
      fill="#7FAFC2"
      font-family="monospace"
      opacity="0">
  REPOS
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="5.95s"
           fill="freeze"/>
</text>

<text x="700" y="330"
      fill="#7FAFC2"
      font-family="monospace"
      font-size="24"
      opacity="0">
  {s['repos']}
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="6.05s"
           fill="freeze"/>
</text>

<!-- STARS -->
<text x="700" y="380"
      fill="#7FAFC2"
      font-family="monospace"
      opacity="0">
  STARS
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="6.15s"
           fill="freeze"/>
</text>

<text x="700" y="410"
      fill="#7FAFC2"
      font-family="monospace"
      font-size="24"
      opacity="0">
  {s['stars']}
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="6.25s"
           fill="freeze"/>
</text>

<!-- FOLLOWERS -->
<text x="700" y="460"
      fill="#7FAFC2"
      font-family="monospace"
      opacity="0">
  FOLLOWERS
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="6.35s"
           fill="freeze"/>
</text>

<text x="700" y="490"
      fill="#7FAFC2"
      font-family="monospace"
      font-size="24"
      opacity="0">
  {s['followers']}
  <animate attributeName="opacity"
           from="0" to="1"
           dur="0.2s"
           begin="6.45s"
           fill="freeze"/>
</text>
  <!-- SCAN + NOISE -->
  <rect x="0" y="-20" width="1000" height="14" fill="#7FAFC2" opacity="0.08">
    <animate attributeName="y" values="-20;620" dur="2.6s" repeatCount="indefinite"/>
  </rect>

  <rect width="1000" height="600" filter="url(#noise)" opacity="0.05"/>

  <rect width="1000" height="600" fill="#7FAFC2" opacity="0">
    <animate attributeName="opacity" values="0;0.015;0" dur="4s" repeatCount="indefinite"/>
  </rect>

</g>  
</svg>
"""


def main():
    stats = get_stats()
    svg = build_svg(stats)

    os.makedirs("output", exist_ok=True)

    with open("output/dashboard.svg", "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    main()