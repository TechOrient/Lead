# Deep Research System Summary and Architecture

# TAVILY API KEY KULLANIMDA DEĞİL AGENT'LAR ARAŞTIRAMIYOR 

## Özet: Sistem Akışı
- Kullanıcı Input → Soru netleştirme
- Research Brief → Araştırma konusu yapılandırma
- Supervisor → Araştırma planı ve task dağıtımı
- Parallel Researchers → Her konu için bağımsız araştırma
- Compression → Her araştırmayı özetleme
- Final Report → Tüm bulguları tek raporda birleştirme



## Clarifiy_with_user fonksiyonu 

Kullanıcıdan gelen soruyu ya da prompt'u yeterince net olup olmadığını kontrol eder 

#### Detaylar: 
- allow_clarification ayarı kontrol edilir 
- Eğer kapalıysa arama sürecine başlar
- Açıksa LLM kullanımı ile soruyu analiz eder ve ClarifiyWithUSer structured output'u üretir
- need_clarification = True -> Kullanıcıya soruyu sorar ve biter
- need_clarification = False -> Research brief oluşturmaya geçer

* Agent Prompt -> clarifiy_with_user_instructions

* Retry Logic -> max-structured_output_retries -> deneme sayısı 


## Research Brief Creation (Araştırma Planı Oluşturma)

- Kullanıcının mesajlarını yapılandırılmış bir araştırma konusuna dönüşür
- Kullanıcının tüm mesajlarını alır state["messages"]
- transform_messages_into_research_topic_prompt promptu kullanarak LLM'e gönderir
- ResearchQuestion structured output üretir (research_brief içerir)
- Supervisior için sistem promptu hazırlar (lead_researcher_prompt)

* max_concurrent_research_units: Paralel kaç araştırma birimi çalışabilir
* max_researcher_iterations: Maksimum araştırma iterasyonu



## Research Execution Phase (Araştırma Yürütme)

- Bu aşama Supervisor-Researcher hiyeraşiyle çalışır

### A. Supervisor Subgraph
- Supervisor Fonksiyonu


- Görev: Araştırmayı yöneten baş araştırmacı. Araştırma stratejisi belirler ve alt - araştırmacılara görev dağıtır.


#### Kullanabileceği Araçlar:

- think_tool: Stratejik düşünme ve planlama yapar
- ConductResearch: Alt araştırmacılara araştırma konusu atar
- ResearchComplete: Araştırmanın tamamlandığını bildirirç

#### Akış:

- supervisor_messages state'ini analiz eder
- LLM'e tool call yapma yetkisi verir
- research_iterations sayacını artırır
- Supervisor tools'a geçer


- supervisor_tools fonksiyonu 

- Görev : supervisor'un çağırdığı araçlar çalıştırır

- Detaylı mantık

Exit Koşulları (Araştırma sona erer):

research_iterations > max_researcher_iterations
Tool call yoksa
ResearchComplete çağrıldıysa

Tool Execution:

think_tool İşleme:

Reflection içeriğini alır
ToolMessage olarak geri döner
Sadece loglanır, araştırma başlatmaz


ConductResearch İşleme:

Maksimum max_concurrent_research_units kadar paralel araştırma başlatır
Her araştırma için researcher_subgraph.ainvoke() çağrısı yapar
asyncio.gather() ile paralel çalıştırır
Fazla görevler için hata mesajı döner
Her araştırmanın sonucunu (compressed_research) ToolMessage olarak döner
Tüm raw_notes'ları birleştirir

Error Handling:

Token limit aşımı kontrolü (is_token_limit_exceeded)
Hata durumunda araştırmayı sonlandırır


### B. Researcher Subgraph 
- Her araştırma görevi için ayrı bir researcher instance çalışır

- researcher Fonksiyonu()

Görev : Belirli bir konuda odaklanmış araştırma yapar. 

Kullanabileceği Araçlar:
- get_all_tools(config) ile dinamik tool listesi:
- Web Search tools(Tavily,Brave, SerpAPI eklenecek)
- MCP Tools (harici entegrasyonlar)
- think_tool

##### Akış
- Tool'lar yüklenir (yoksa hata verir)
- Research model'i bind_tools ile yapılandırır
- System prompt research_system_prompt (MCP prompt dahil)
- LLM tool call yapma yetkisi verir 
- tool_call_iterations sayacı arttırılır
- Researcher tools'a geçer
- .
- MCP Integration 
- mcp_prompt configuration'dan gelir (dosya)
- Harici tool'ları dinamik olarak sisteme ekler


#### researcher_tools fonksiyonu 

Researcher çağırdığı tüm tool'ları güvenli şekilde çalıştırır

###### Detaylı Akış

- Early Exit Check:

Tool call yoksa VE native web search yoksa → compress_research'e geç

Native Web Search Detection:

OpenAI'nin built-in web search: openai_websearch_called()
Anthropic'in built-in web search: anthropic_websearch_called()
Bu durumda tool_calls boş olsa bile devam eder

Tool Execution:

execute_tool_safely() ile her tool parallel çalıştırılır
asyncio.gather() ile tüm tool'lar aynı anda execute edilir
Her tool sonucu ToolMessage'a dönüştürülür

Late Exit Check (Tool'lar çalıştıktan sonra):

tool_call_iterations >= max_react_tool_calls → compress'e geç
ResearchComplete çağrıldıysa → compress'e geç


Late Exit Check (Tool'lar çalıştıktan sonra):

tool_call_iterations >= max_react_tool_calls → compress'e geç
ResearchComplete çağrıldıysa → compress'e geç

Aksi halde : Researcher geri dönüp yeni tool'lar call'lar yapar



### compress_research fonksiyonu 
- Tüm araştırma bulgularını özelter ve sıkıştırır 

- Detaylı Mantık

Input > 
- researcher_messages : Tüm AI ve tool mesajları içerir

- compress_research_simple_human_message ile instruction eklenir

- compression model kullanılır

- System Prompt -> compress_research_system_prompt

#### Retry Logic 
- Max 3 deneme var 
- Token limit aşımında remove_up_to_last_ai_message() ile eski mesajları siler

- Her denemede mesaj geçmişi kısaltılır

Output >

- compressed_research : Özet Rapor
- raw_notes : Ham araştırma verileri

- Error Handling
- 3 deneme sonrası : Maxiumum retries exceeded" hatası döner 



### Final Report Generation 

- final_report_generation fonksiyonu 

Input >
- notes : Supervisor'ın topladığı tüm compressed researchler
- research_brief : Orijinal araştırma sorusu 
- messages : kullanıcı mesaj geçmişi 


- Detaylı Mantık 

- final_report_generation : kullanluılır (en güçlü model toplama için kullanılır)

- final_report_model_max_tokens : token limiti ayarlanır 


