import os
import re
import requests
import shutil

# List of GitHub project URLs for JavaScript (Node.js/NPM) projects.
javascript_projects = [
    "https://github.com/facebook/react",
    "https://github.com/trekhleb/javascript-algorithms",
    "https://github.com/twbs/bootstrap",
    "https://github.com/airbnb/javascript",
    "https://github.com/vercel/next.js",
    "https://github.com/Chalarangelo/30-seconds-of-code",
    "https://github.com/nodejs/node",
    "https://github.com/axios/axios",
    "https://github.com/mrdoob/three.js",
    "https://github.com/facebook/create-react-app",
    "https://github.com/ryanmcdermott/clean-code-javascript",
    "https://github.com/iptv-org/iptv",
    "https://github.com/microsoft/Web-Dev-For-Beginners",
    "https://github.com/sveltejs/svelte",
    "https://github.com/jaywcjlove/awesome-mac",
    "https://github.com/FortAwesome/Font-Awesome",
    "https://github.com/typicode/json-server",
    "https://github.com/anuraghazra/github-readme-stats",
    "https://github.com/hakimel/reveal.js",
    "https://github.com/expressjs/express",
    "https://github.com/open-webui/open-webui",
    "https://github.com/chartjs/Chart.js",
    "https://github.com/webpack/webpack",
    "https://github.com/leonardomso/33-js-concepts",
    "https://github.com/louislam/uptime-kuma",
    "https://github.com/resume/resume.github.com",
    "https://github.com/atom/atom",
    "https://github.com/lodash/lodash",
    "https://github.com/adam-p/markdown-here",
    "https://github.com/jquery/jquery",
    "https://github.com/angular/angular.js",
    "https://github.com/h5bp/html5-boilerplate",
    "https://github.com/gatsbyjs/gatsby",
    "https://github.com/scutan90/DeepLearning-500-questions",
    "https://github.com/azl397985856/leetcode",
    "https://github.com/jgraph/drawio-desktop",
    "https://github.com/Semantic-Org/Semantic-UI",
    "https://github.com/juliangarnier/anime",
    "https://github.com/prettier/prettier",
    "https://github.com/mozilla/pdf.js",
    "https://github.com/gorhill/uBlock",
    "https://github.com/chinese-poetry/chinese-poetry",
    "https://github.com/marktext/marktext",
    "https://github.com/TryGhost/Ghost",
    "https://github.com/moment/moment",
    "https://github.com/NARKOZ/hacker-scripts",
    "https://github.com/cypress-io/cypress",
    "https://github.com/iamkun/dayjs",
    "https://github.com/poteto/hiring-without-whiteboards",
    "https://github.com/algorithm-visualizer/algorithm-visualizer",
    "https://github.com/serverless/serverless",
    "https://github.com/agalwood/Motrix",
    "https://github.com/typescript-cheatsheets/react",
    "https://github.com/meteor/meteor",
    "https://github.com/Asabeneh/30-Days-Of-JavaScript",
    "https://github.com/parcel-bundler/parcel",
    "https://github.com/google/zx",
    "https://github.com/bigskysoftware/htmx",
    "https://github.com/Leaflet/Leaflet",
    "https://github.com/Unitech/pm2",
    "https://github.com/yarnpkg/yarn",
    "https://github.com/GitSquared/edex-ui",
    "https://github.com/LeCoupa/awesome-cheatsheets",
    "https://github.com/microsoft/monaco-editor",
    "https://github.com/sudheerj/reactjs-interview-questions",
    "https://github.com/nwjs/nw.js",
    "https://github.com/nolimits4web/swiper",
    "https://github.com/dcloudio/uni-app",
    "https://github.com/Dogfalo/materialize",
    "https://github.com/videojs/video.js",
    "https://github.com/impress/impress.js",
    "https://github.com/phaserjs/phaser",
    "https://github.com/NaiboWang/EasySpider",
    "https://github.com/preactjs/preact",
    "https://github.com/denysdovhan/wtfjs",
    "https://github.com/naptha/tesseract.js",
    "https://github.com/Kong/insomnia",
    "https://github.com/alvarotrigo/fullPage.js",
    "https://github.com/koajs/koa",
    "https://github.com/sahat/hackathon-starter",
    "https://github.com/jondot/awesome-react-native",
    "https://github.com/carbon-app/carbon",
    "https://github.com/goabstract/Awesome-Design-Tools",
    "https://github.com/zenorocha/clipboard.js",
    "https://github.com/ToolJet/ToolJet",
    "https://github.com/markedjs/marked",
    "https://github.com/atlassian/react-beautiful-dnd",
    "https://github.com/adobe/brackets",
    "https://github.com/gulpjs/gulp",
    "https://github.com/typicode/husky",
    "https://github.com/fastify/fastify",
    "https://github.com/TheAlgorithms/JavaScript",
    "https://github.com/Mintplex-Labs/anything-llm",
    "https://github.com/ryanhanwu/How-To-Ask-Questions-The-Smart-Way",
    "https://github.com/qishibo/AnotherRedisDesktopManager",
    "https://github.com/pcottle/learnGitBranching",
    "https://github.com/airbnb/lottie-web",
    "https://github.com/remoteintech/remote-jobs",
    "https://github.com/usebruno/bruno",
    "https://github.com/gchq/CyberChef",
]

# Name of the new folder
folder_name = "javascript projects 2"

# Remove the old folder if it exists, then create a new one.
if os.path.exists(folder_name):
    shutil.rmtree(folder_name)
os.makedirs(folder_name, exist_ok=True)

def parse_github_url(url):
    """
    Extracts the owner and repo name from a GitHub URL.
    """
    url = url.split("#")[0].strip()  # Remove any fragment identifiers
    pattern = r"github\.com/([^/]+)/([^/]+)"
    match = re.search(pattern, url)
    if match:
        owner, repo = match.groups()
        repo = repo.replace(".git", "")
        return owner, repo
    return None, None

def download_package_json(owner, repo, folder):
    """
    Attempts to download package.json from the repository by trying the 'master' branch,
    then the 'main' branch if needed.
    """
    for branch in ["master", "main"]:
        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/package.json"
        r = requests.get(raw_url)
        if r.status_code == 200 and r.text.strip():
            file_path = os.path.join(folder, f"{repo}-package.json")
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(r.text)
            print(f"Downloaded package.json from {owner}/{repo} (branch: {branch})")
            return True
    print(f"Could not find package.json for {owner}/{repo}")
    return False

# Process each project URL.
for url in javascript_projects:
    owner, repo = parse_github_url(url)
    if owner and repo:
        download_package_json(owner, repo, folder_name)
    else:
        print(f"Could not parse URL: {url}")
