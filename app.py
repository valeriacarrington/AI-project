from flask import Flask, render_template_string, request, jsonify
import openai
import os
import json
from datetime import datetime

app = Flask(__name__)

# API Key - ЗАМІНІТЬ!
openai.api_key = os.environ.get('OPENAI_API_KEY', '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')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🚀 Генератор Стартапів</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
            border-radius: 20px 20px 0 0;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .content { padding: 40px; }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
        }
        .tab {
            padding: 15px 30px;
            background: none;
            border: none;
            border-bottom: 3px solid transparent;
            cursor: pointer;
            font-size: 1.1em;
            font-weight: 600;
            color: #666;
            transition: all 0.3s;
        }
        .tab:hover { color: #667eea; }
        .tab.active {
            color: #667eea;
            border-bottom-color: #667eea;
        }
        
        .tab-content { display: none; }
        .tab-content.active { display: block; }
        
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            margin: 15px 0;
            resize: vertical;
        }
        textarea:focus {
            outline: none;
            border-color: #667eea;
        }
        
        .tags-container {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 15px 0;
        }
        .tag {
            background: #667eea;
            color: white;
            padding: 8px 15px;
            border-radius: 20px;
            font-size: 0.9em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .tag-remove {
            cursor: pointer;
            font-weight: bold;
            font-size: 1.2em;
        }
        .tag-input {
            padding: 8px 15px;
            border: 2px solid #e0e0e0;
            border-radius: 20px;
        }
        
        .button-group {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .btn {
            padding: 18px;
            font-size: 1.1em;
            font-weight: 600;
            color: white;
            border: none;
            border-radius: 10px;
            cursor: pointer;
            transition: all 0.3s;
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(0,0,0,0.2);
        }
        .btn-analyze { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); }
        .btn-search { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
        .btn-success { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
        .btn-primary { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        
        .result-card {
            background: #f8f9fa;
            border-radius: 15px;
            padding: 30px;
            margin-top: 20px;
        }
        .startup-name {
            font-size: 2.5em;
            color: #667eea;
            font-weight: 700;
            margin-bottom: 10px;
        }
        .startup-tagline {
            font-size: 1.3em;
            color: #666;
            font-style: italic;
            margin-bottom: 20px;
        }
        .section {
            margin: 20px 0;
            padding: 15px;
            background: white;
            border-radius: 10px;
        }
        .section h3 {
            color: #667eea;
            margin-bottom: 10px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin: 20px 0;
        }
        .metric-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #e0e0e0;
        }
        .metric-value {
            font-size: 2em;
            font-weight: 700;
            color: #667eea;
        }
        .metric-label {
            font-size: 0.9em;
            color: #666;
            margin-top: 5px;
        }
        
        .loading {
            text-align: center;
            padding: 40px;
            color: #667eea;
        }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 20px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        select {
            width: 100%;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 1em;
            margin: 15px 0;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 Генератор Стартапів</h1>
            <p>Аналізуйте ідеї • Генеруйте стартапи • Знаходьте конкурентів</p>
        </div>
        
        <div class="content">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('analyze')">🔍 Аналіз ідеї</button>
                <button class="tab" onclick="switchTab('generate')">✨ Генератор</button>
            </div>
            
            <!-- Tab 1: Analyze -->
            <div class="tab-content active" id="tab-analyze">
                <h2>🔍 Аналіз вашої бізнес-ідеї</h2>
                
                <label><strong>✍️ Опис вашої ідеї:</strong></label>
                <textarea id="ideaText" placeholder="Опишіть вашу бізнес-ідею детально..."></textarea>
                
                <label><strong>🏷️ Теги (Enter щоб додати):</strong></label>
                <div class="tags-container" id="tagsContainer">
                    <input type="text" class="tag-input" id="tagInput" placeholder="Додати тег...">
                </div>
                
                <div class="button-group">
                    <button class="btn btn-analyze" onclick="analyzeIdea()">
                        🔍 Проаналізувати ідею
                    </button>
                    <button class="btn btn-search" onclick="searchCompetitors()">
                        🌐 Знайти конкурентів
                    </button>
                    <button class="btn btn-success" onclick="generateFromIdea()">
                        ✨ Згенерувати стартап
                    </button>
                </div>
                
                <div id="analysisResults"></div>
            </div>
            
            <!-- Tab 2: Generate -->
            <div class="tab-content" id="tab-generate">
                <h2>✨ Генератор стартапів</h2>
                
                <label><strong>✍️ Додаткові вимоги (опціонально):</strong></label>
                <textarea id="customPrompt" placeholder="Наприклад: 'Для покоління Z', 'B2B сегмент'..."></textarea>
                
                <label><strong>Оберіть індустрію:</strong></label>
                <select id="industry">
                    <option value="random">🎲 Випадкова</option>
                    <option value="fintech">💰 Фінтех</option>
                    <option value="healthtech">🏥 Медтех</option>
                    <option value="edtech">📚 Едтех</option>
                    <option value="foodtech">🍕 Фудтех</option>
                    <option value="ai">🤖 AI/ML</option>
                    <option value="blockchain">⛓️ Блокчейн</option>
                    <option value="sustainability">🌱 Екологія</option>
                </select>
                
                <label style="display: flex; align-items: center; gap: 10px; margin: 15px 0;">
                    <input type="checkbox" id="generateLogo" style="width: 20px; height: 20px;">
                    <span>🎨 Згенерувати логотип через DALL-E</span>
                </label>
                
                <div class="button-group">
                    <button class="btn btn-primary" onclick="generateStartup()">
                        ✨ Згенерувати Стартап
                    </button>
                </div>
                
                <div id="startupResults"></div>
            </div>
        </div>
    </div>
    
    <script>
        let currentTags = [];
        let currentStartup = null;
        
        // Tabs
        function switchTab(tabName) {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            
            event.target.classList.add('active');
            document.getElementById('tab-' + tabName).classList.add('active');
        }
        
        // Tags
        document.getElementById('tagInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                const tag = e.target.value.trim();
                if (tag && !currentTags.includes(tag)) {
                    currentTags.push(tag);
                    updateTags();
                    e.target.value = '';
                }
            }
        });
        
        function removeTag(tag) {
            currentTags = currentTags.filter(t => t !== tag);
            updateTags();
        }
        
        function updateTags() {
            const container = document.getElementById('tagsContainer');
            const input = document.getElementById('tagInput');
            
            container.innerHTML = '';
            currentTags.forEach(tag => {
                const tagEl = document.createElement('div');
                tagEl.className = 'tag';
                tagEl.innerHTML = tag + ' <span class="tag-remove" onclick="removeTag(\\'' + tag + '\\')">×</span>';
                container.appendChild(tagEl);
            });
            container.appendChild(input);
        }
        
        function showLoading(elementId) {
            document.getElementById(elementId).innerHTML = '<div class="loading"><div class="spinner"></div><p>⏳ Завантаження...</p></div>';
        }
        
        async function regenerateLogo() {
            if (!currentStartup) {
                alert('❌ Спочатку згенеруйте стартап');
                return;
            }
            
            const customPrompt = prompt('Опишіть що ви хочете бачити на логотипі (або залиште порожнім для автоматичної генерації):', '');
            
            try {
                const response = await fetch('/api/regenerate-logo', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        name: currentStartup.name,
                        tagline: currentStartup.tagline,
                        custom_prompt: customPrompt || ''
                    })
                });
                
                const data = await response.json();
                
                if (data.logo_image) {
                    const logoImg = document.getElementById('startupLogo');
                    if (logoImg) {
                        logoImg.src = data.logo_image;
                        currentStartup.logo_image = data.logo_image;
                        alert('✅ Логотип оновлено!');
                    }
                } else if (data.error) {
                    alert('❌ Помилка: ' + data.error);
                }
            } catch (error) {
                alert('❌ Помилка: ' + error.message);
            }
        }
        
        // API Calls
        async function analyzeIdea() {
            const idea = document.getElementById('ideaText').value.trim();
            if (!idea) { alert('❌ Введіть опис ідеї'); return; }
            
            showLoading('analysisResults');
            
            try {
                const response = await fetch('/api/analyze', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({idea, tags: currentTags})
                });
                
                const data = await response.json();
                
                document.getElementById('analysisResults').innerHTML = `
                    <div class="result-card">
                        <h2>📊 Результати аналізу</h2>
                        <div class="section">
                            <h3>💡 Оцінка</h3>
                            <p>${data.evaluation || 'N/A'}</p>
                        </div>
                        <div class="section">
                            <h3>📈 Потенціал ринку</h3>
                            <p>${data.market_potential || 'N/A'}</p>
                        </div>
                        <div class="section">
                            <h3>⚠️ Ризики</h3>
                            <p>${data.risks || 'N/A'}</p>
                        </div>
                        <div class="section">
                            <h3>💪 Рекомендації</h3>
                            <p>${data.recommendations || 'N/A'}</p>
                        </div>
                    </div>
                `;
            } catch (error) {
                alert('❌ Помилка: ' + error.message);
                document.getElementById('analysisResults').innerHTML = '';
            }
        }
        
        async function searchCompetitors() {
            const idea = document.getElementById('ideaText').value.trim();
            if (!idea) { alert('❌ Введіть опис ідеї'); return; }
            
            showLoading('analysisResults');
            
            try {
                const response = await fetch('/api/search-competitors', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({idea})
                });
                
                const data = await response.json();
                
                let html = '<div class="result-card"><h2>🔍 Конкуренти</h2>';
                
                data.competitors.forEach(c => {
                    html += `
                        <div class="section">
                            <h3>${c.name || 'Конкурент'}</h3>
                            <p><strong>Опис:</strong> ${c.description || 'N/A'}</p>
                            <p><strong>Сильні сторони:</strong> ${c.strengths || 'N/A'}</p>
                            <p><strong>Відмінності:</strong> ${c.differences || 'N/A'}</p>
                        </div>
                    `;
                });
                
                html += `<div class="section"><h3>💡 Висновок</h3><p>${data.conclusion || 'N/A'}</p></div></div>`;
                
                document.getElementById('analysisResults').innerHTML = html;
            } catch (error) {
                alert('❌ Помилка: ' + error.message);
                document.getElementById('analysisResults').innerHTML = '';
            }
        }
        
        async function generateFromIdea() {
            const idea = document.getElementById('ideaText').value.trim();
            if (!idea) { alert('❌ Введіть опис ідеї'); return; }
            
            showLoading('analysisResults');
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        industry: 'random',
                        custom_prompt: 'На основі ідеї: ' + idea,
                        crazy_mode: false,
                        generate_logo: false
                    })
                });
                
                const startup = await response.json();
                displayStartup(startup, 'analysisResults');
            } catch (error) {
                alert('❌ Помилка: ' + error.message);
                document.getElementById('analysisResults').innerHTML = '';
            }
        }
        
        async function generateStartup() {
            const industry = document.getElementById('industry').value;
            const customPrompt = document.getElementById('customPrompt').value;
            const generateLogo = document.getElementById('generateLogo').checked;
            
            showLoading('startupResults');
            
            try {
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        industry,
                        custom_prompt: customPrompt,
                        crazy_mode: false,
                        generate_logo: generateLogo
                    })
                });
                
                const startup = await response.json();
                displayStartup(startup, 'startupResults');
            } catch (error) {
                alert('❌ Помилка: ' + error.message);
                document.getElementById('startupResults').innerHTML = '';
            }
        }
        
        function displayStartup(s, containerId) {
            currentStartup = s;  // Save for regeneration
            
            const logoHtml = s.logo_image 
                ? `<img src="${s.logo_image}" style="width: 200px; height: 200px; border-radius: 10px; border: 2px solid #e0e0e0; object-fit: cover;" id="startupLogo">`
                : `<div style="background: white; padding: 20px; border: 2px solid #e0e0e0; border-radius: 10px; font-family: monospace; white-space: pre;">${s.logo || ''}</div>`;
            
            document.getElementById(containerId).innerHTML = `
                <div class="result-card">
                    <div style="display: flex; gap: 30px; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 2px solid #e0e0e0;">
                        <div>
                            ${logoHtml}
                            <button class="btn btn-primary" style="margin-top: 10px; padding: 10px; font-size: 0.9em;" onclick="regenerateLogo()">
                                🔄 Новий логотип
                            </button>
                        </div>
                        <div style="flex: 1;">
                            <div class="startup-name">${s.name}</div>
                            <div class="startup-tagline">"${s.tagline}"</div>
                        </div>
                    </div>
                    
                    <div class="metrics-grid">
                        <div class="metric-card">
                            <div class="metric-value">${s.metrics?.valuation || 'N/A'}</div>
                            <div class="metric-label">Валюація</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${s.metrics?.arr || 'N/A'}</div>
                            <div class="metric-label">ARR</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${s.metrics?.users || 'N/A'}</div>
                            <div class="metric-label">Користувачів</div>
                        </div>
                        <div class="metric-card">
                            <div class="metric-value">${s.metrics?.runway || 'N/A'}</div>
                            <div class="metric-label">Runway</div>
                        </div>
                    </div>
                    
                    <div class="section">
                        <h3>📝 Опис</h3>
                        <p>${s.description}</p>
                    </div>
                    
                    <div class="section">
                        <h3>🎯 Elevator Pitch</h3>
                        <p>${s.pitch}</p>
                    </div>
                    
                    <div class="section">
                        <h3>👥 Команда</h3>
                        <p>${s.team || 'N/A'}</p>
                    </div>
                    
                    <div class="section">
                        <h3>🎯 Цільова аудиторія</h3>
                        <p>${s.audience || 'N/A'}</p>
                    </div>
                    
                    <div class="section">
                        <h3>💰 Бізнес-модель</h3>
                        <p>${s.business_model || 'N/A'}</p>
                    </div>
                </div>
            `;
        }
    </script>
</body>
</html>
'''

FAVORITES_FILE = 'favorites.json'

def load_json(filename):
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    return []

def save_json(filename, data):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def generate_startup(industry, crazy_mode, generate_logo, custom_prompt):
    industries = {
        'random': 'випадкову', 'fintech': 'фінтех', 'healthtech': 'медтех',
        'edtech': 'едтех', 'foodtech': 'фудтех', 'ai': 'AI',
        'blockchain': 'блокчейн', 'sustainability': 'екологію'
    }
    
    industry_text = industries.get(industry, 'випадкову')
    suffix = f"\nДодатково: {custom_prompt}" if custom_prompt else ""
    
    prompt = f"""Створи стартап у сфері {industry_text}.{suffix}

НАЗВА: [англійською 1-2 слова]
СЛОГАН: [українською 5-10 слів]
ОПИС: [4-5 речень]
ПІТЧ: [5-7 речень]
КОМАНДА: [3-4 особи]
ЦІЛЬОВА_АУДИТОРІЯ: [2-3 речення]
БІЗНЕС_МОДЕЛЬ: [2-3 речення]
КОНКУРЕНТИ: [2-3]
ВАЛЮАЦІЯ: [сума]
ARR: [сума]
КОРИСТУВАЧІ: [число]
RUNWAY: [місяці]"""

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти венчурний інвестор."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.85,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content.strip()
        
        startup = {}
        key_map = {
            'НАЗВА:': 'name', 'СЛОГАН:': 'tagline', 'ОПИС:': 'description',
            'ПІТЧ:': 'pitch', 'КОМАНДА:': 'team', 'ЦІЛЬОВА_АУДИТОРІЯ:': 'audience',
            'БІЗНЕС_МОДЕЛЬ:': 'business_model', 'КОНКУРЕНТИ:': 'competitors',
            'ВАЛЮАЦІЯ:': 'valuation', 'ARR:': 'arr', 
            'КОРИСТУВАЧІ:': 'users', 'RUNWAY:': 'runway'
        }
        
        current_key = None
        current_value = []
        
        for line in content.split('\n'):
            line = line.strip()
            if not line: continue
            
            found = False
            for marker, key in key_map.items():
                if line.startswith(marker):
                    if current_key and current_value:
                        startup[current_key] = ' '.join(current_value).strip()
                    current_key = key
                    current_value = [line.replace(marker, '').strip()]
                    found = True
                    break
            
            if not found and current_key:
                current_value.append(line)
        
        if current_key and current_value:
            startup[current_key] = ' '.join(current_value).strip()
        
        startup['metrics'] = {
            'valuation': startup.get('valuation', '$10M'),
            'arr': startup.get('arr', '$2M'),
            'users': startup.get('users', '100K'),
            'runway': startup.get('runway', '18 міс')
        }
        
        # Generate logo via DALL-E if requested
        if generate_logo:
            try:
                logo_prompt = f"A modern, minimalist, professional logo for a tech startup called '{startup.get('name', 'Startup')}'. {startup.get('tagline', '')}. Simple, clean design, suitable for a tech company. No text in the image."
                
                logo_response = openai.images.generate(
                    model="dall-e-3",
                    prompt=logo_prompt,
                    size="1024x1024",
                    quality="standard",
                    n=1,
                )
                
                startup['logo_image'] = logo_response.data[0].url
            except Exception as e:
                print(f"Logo generation error: {e}")
                startup['logo_image'] = None
        else:
            startup['logo_image'] = None
        
        return startup
    except Exception as e:
        return {
            'name': 'Error', 'tagline': 'Помилка',
            'description': str(e), 'pitch': 'Перевірте API ключ',
            'team': 'N/A', 'audience': 'N/A', 'business_model': 'N/A',
            'competitors': 'N/A', 'metrics': {'valuation': 'N/A', 'arr': 'N/A', 'users': 'N/A', 'runway': 'N/A'}
        }

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    startup = generate_startup(
        data.get('industry', 'random'),
        data.get('crazy_mode', False),
        data.get('generate_logo', False),
        data.get('custom_prompt', '')
    )
    return jsonify(startup)

@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    data = request.json
    idea = data.get('idea', '')
    
    try:
        prompt = f"""Проаналізуй ідею: {idea}

СХОЖІСТЬ: [high/medium/low]
ОЦІНКА: [детально]
ПОТЕНЦІАЛ: [детально]
РИЗИКИ: [детально]
РЕКОМЕНДАЦІЇ: [детально]"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти бізнес-аналітик."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        content = response.choices[0].message.content
        result = {
            'similarity_level': 'medium',
            'evaluation': '', 'market_potential': '',
            'risks': '', 'recommendations': ''
        }
        
        for line in content.split('\n'):
            line = line.strip()
            if line.startswith('ОЦІНКА:'):
                result['evaluation'] = line.split(':', 1)[1].strip()
            elif line.startswith('ПОТЕНЦІАЛ:'):
                result['market_potential'] = line.split(':', 1)[1].strip()
            elif line.startswith('РИЗИКИ:'):
                result['risks'] = line.split(':', 1)[1].strip()
            elif line.startswith('РЕКОМЕНДАЦІЇ:'):
                result['recommendations'] = line.split(':', 1)[1].strip()
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/search-competitors', methods=['POST'])
def api_search_competitors():
    data = request.json
    idea = data.get('idea', '')
    
    try:
        prompt = f"""Знайди 3-5 конкурентів для: {idea}

НАЗВА: [назва]
ОПИС: [опис]
СИЛЬНІ_СТОРОНИ: [переваги]
ВІДМІННОСТІ: [відмінності]

ВИСНОВОК: [загальний]"""
        
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ти аналітик ринку."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500
        )
        
        content = response.choices[0].message.content
        
        competitors = []
        current = {}
        conclusion = ''
        in_conclusion = False
        
        for line in content.split('\n'):
            line = line.strip()
            
            if line.startswith('ВИСНОВОК:'):
                in_conclusion = True
                conclusion = line.split(':', 1)[1].strip()
                continue
            
            if in_conclusion:
                conclusion += ' ' + line
                continue
            
            if line.startswith('НАЗВА:'):
                if current: competitors.append(current)
                current = {'name': line.split(':', 1)[1].strip()}
            elif line.startswith('ОПИС:'):
                current['description'] = line.split(':', 1)[1].strip()
            elif line.startswith('СИЛЬНІ_СТОРОНИ:'):
                current['strengths'] = line.split(':', 1)[1].strip()
            elif line.startswith('ВІДМІННОСТІ:'):
                current['differences'] = line.split(':', 1)[1].strip()
        
        if current: competitors.append(current)
        
        return jsonify({'competitors': competitors, 'conclusion': conclusion})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/regenerate-logo', methods=['POST'])
def api_regenerate_logo():
    """Regenerate logo with DALL-E"""
    data = request.json
    name = data.get('name', 'Startup')
    tagline = data.get('tagline', '')
    custom_prompt = data.get('custom_prompt', '')
    
    try:
        prompt_text = f"A modern, minimalist, professional logo for a tech startup called '{name}'. {tagline}. Simple, clean design. No text in the image."
        if custom_prompt:
            prompt_text = f"A logo for '{name}': {custom_prompt}. Professional, modern design. No text."
        
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt_text,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        
        return jsonify({'logo_image': response.data[0].url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Запуск...")
    print("🌐 http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)