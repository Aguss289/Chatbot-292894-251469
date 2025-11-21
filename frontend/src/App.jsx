import React, {useState} from 'react'


export default function App(){
const [q, setQ] = useState('')
const [ans, setAns] = useState(null)
const [loading, setLoading] = useState(false)


async function ask(){
setLoading(true)
const res = await fetch('/api/query', {
method: 'POST',
headers: {'Content-Type':'application/json'},
body: JSON.stringify({question: q})
})
const j = await res.json()
setAns(j)
setLoading(false)
}


return (
<div style={{maxWidth:800, margin:'2rem auto'}}>
<h1>Retail360 Chatbot</h1>
<textarea value={q} onChange={(e)=>setQ(e.target.value)} rows={3} style={{width:'100%'}} />
<button onClick={ask} disabled={loading}>Preguntar</button>
{loading && <p>Cargando...</p>}
{ans && (
<div>
<h3>Respuesta</h3>
<p>{ans.answer}</p>
{ans.sources && ans.sources.length>0 && (
<div>
<h4>Fuentes</h4>
<ul>{ans.sources.map((s,i)=>(<li key={i}>{JSON.stringify(s)}</li>))}</ul>
</div>
)}
</div>
)}
</div>
)
}