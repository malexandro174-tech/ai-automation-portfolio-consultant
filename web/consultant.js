const caseTech = {"case-commercial-funnel": ["Python", "PostgreSQL", "observability"], "case-data-analyst": ["Python", "FastAPI", "DeepSeek", "Docker"], "case-employee-training": ["Telegram", "PostgreSQL", "DeepSeek", "Python"], "case-feedback-reputation": ["DeepSeek", "PostgreSQL", "Docker", "Broker"], "case-intake-classifier": ["n8n", "NocoDB", "Telegram", "JSON"], "case-lead-intake": ["Telegram", "SQLite", "Broker", "DeepSeek"], "case-meeting-intelligence": ["AssemblyAI", "DeepSeek", "Telegram", "PostgreSQL", "Docker"], "case-n8n-engineering": ["n8n", "PowerShell", "REST API", "JSON"], "case-public-consultant": ["FastAPI", "Docker", "Nginx"], "case-writer-rag": ["Qdrant", "BGE-M3", "n8n", "Docker"]};
const faqLaunch = document.querySelector('#faq-launch');
const faqPanel = document.querySelector('#faq-panel');
const faqClose = document.querySelector('#faq-close');
const faqForm = document.querySelector('#faq-form');
const faqInput = document.querySelector('#faq-input');
const faqMessages = document.querySelector('#faq-messages');
const faqSuggestions = document.querySelector('#faq-suggestions');
const faqReset = document.querySelector('#faq-reset');
const faqMode = document.querySelector('#faq-mode');
let faqSession = sessionStorage.getItem('mag_rag_session') || crypto.randomUUID().replaceAll('-', '');
sessionStorage.setItem('mag_rag_session', faqSession);
let faqBusy = false;
let faqLastActivity = Date.now();
function toggleFaq(open) { faqPanel.hidden = !open; faqLaunch.setAttribute('aria-expanded', String(open)); if (open) faqInput.focus(); }
function faqMessage(text, cls = 'faq-answer') { const p = document.createElement('p'); p.className = cls; p.textContent = text; faqMessages.append(p); return p; }
function sourceLink(source) {
  try { const url = new URL(source.source_url); if (url.origin !== location.origin || !url.pathname.startsWith('/knowledge/')) return null;
    const a=document.createElement('a');a.href=url.href;a.target='_blank';a.rel='noopener noreferrer';a.textContent=source.title;return a;
  } catch (_) { return null; }
}
function showResult(body) {
  faqMessage(body.answer, body.fallback ? 'faq-fallback' : 'faq-answer');
  if (body.sources?.length) {
    const group=document.createElement('div');group.className='faq-sources';const title=document.createElement('strong');title.textContent='Источники';group.append(title);
    for(const source of body.sources) { const a=sourceLink(source);if(a)group.append(a); }faqMessages.append(group);
  }
  for(const c of (body.matched_cases || []).slice(0,3)) {
    const card=document.createElement('article');card.className='faq-case';const h=document.createElement('strong');h.textContent=c.title;
    const reason=document.createElement('p');reason.textContent=c.why_relevant;card.append(h,reason);
    const tags=document.createElement('small');tags.textContent=(caseTech[c.case_id] || []).filter(t=>t!=='portfolio').join(' · ');card.append(tags);
    const source=body.sources?.find(s=>c.source_ids.includes(s.chunk_id));if(source){const a=sourceLink(source);if(a){a.textContent='Открыть описание кейса';card.append(a);}}faqMessages.append(card);
  }
  if(body.suggested_direction)faqMessage(body.suggested_direction,'faq-direction');
  for(const question of body.follow_up_questions || [])faqMessage(question,'faq-followup');
  if(body.lead_handoff) {
    const button=document.createElement('button');button.type='button';button.className='faq-lead';button.textContent='Обсудить задачу';
    button.addEventListener('click',()=>{toggleFaq(false);document.querySelector('#contact')?.scrollIntoView({behavior:'smooth'});});faqMessages.append(button);
  }
  faqMessages.scrollTop=faqMessages.scrollHeight;
}
async function askFaq(text) {
  const message=text.trim();if(faqBusy || message.length<2 || message.length>1200)return;
  if(Date.now()-faqLastActivity>1800000){faqSession=crypto.randomUUID().replaceAll('-','');sessionStorage.setItem('mag_rag_session',faqSession);}
  faqLastActivity=Date.now();faqBusy=true;faqMessage(message,'faq-question');faqInput.value='';faqInput.disabled=true;
  faqForm.querySelector('button').disabled=true;faqReset.disabled=true;const loading=faqMessage('Ищу источники и проверяю ответ…','faq-loading');
  try {
    const response=await fetch('/api/v2/portfolio-consultant/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:faqSession,message,mode:faqMode.value}),signal:AbortSignal.timeout(29000)});
    const body=await response.json().catch(()=>({}));loading.remove();
    if(!response.ok || !body.success){faqMessage(response.status===429?'Сервис занят или достигнут лимит вопросов. Попробуйте позже.':'Ответ временно недоступен. Повторите вопрос или используйте форму заявки.','faq-error');}
    else showResult(body);
  } catch (_) {loading.textContent='Ответ временно недоступен. Повторите вопрос или используйте форму заявки.';loading.className='faq-error';}
  finally {faqBusy=false;faqInput.disabled=false;faqForm.querySelector('button').disabled=false;faqReset.disabled=false;faqInput.focus();faqMessages.scrollTop=faqMessages.scrollHeight;}
}
faqLaunch?.addEventListener('click',()=>toggleFaq(true));faqClose?.addEventListener('click',()=>toggleFaq(false));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!faqPanel.hidden){toggleFaq(false);faqLaunch.focus();}});
faqForm?.addEventListener('submit',event=>{event.preventDefault();askFaq(faqInput.value);});
faqSuggestions?.addEventListener('click',event=>{if(event.target.matches('button'))askFaq(event.target.textContent);});
faqReset?.addEventListener('click',async()=>{if(faqBusy)return;const previous=faqSession;faqSession=crypto.randomUUID().replaceAll('-','');sessionStorage.setItem('mag_rag_session',faqSession);faqMessages.replaceChildren();faqMessage('Диалог очищен. Задайте вопрос о портфолио или опишите задачу.');try{await fetch('/api/v2/portfolio-consultant/session/clear',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({session_id:previous})});}catch(_){}faqInput.focus();});
