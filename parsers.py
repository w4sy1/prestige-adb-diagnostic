import re
from collections import Counter

def logcat_summary(text):
    counts=Counter();first=None;last=None;unparsed=0
    pattern=re.compile(r'^(\d\d-\d\d\s+\d\d:\d\d:\d\d\.\d+)\s+\d+\s+\d+\s+([EF])\s+([^:]{1,120}):')
    for line in text.splitlines():
        if not line or line.startswith('---------'):continue
        match=pattern.match(line)
        if not match:unparsed+=1;continue
        stamp,priority,tag=match.groups();tag=tag.strip()
        # Nie zapisujemy wiadomości, PID ani identyfikatorów urządzenia.
        counts[(priority,tag)]+=1;first=first or stamp;last=stamp
    return {'groups':[{'priority':priority,'tag':tag,'count':count} for (priority,tag),count in counts.most_common(50)],
            'total_errors':sum(counts.values()),'first_timestamp':first,'last_timestamp':last,'unparsed_lines':unparsed,'messages_stored':False}

def permissions_summary(text):
    granted={name:value=='true' for name,value in re.findall(r'(android\.permission\.[A-Z_0-9]+):\s*granted=(true|false)',text)}
    return {'permissions':granted,'source':'dumpsys package','complete':bool(granted)}
