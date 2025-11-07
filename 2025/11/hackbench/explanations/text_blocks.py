"""
Educational text blocks and explanations for XSS concepts.
Referenced throughout the tool to teach users about XSS vulnerabilities.
"""


class XSSExplanations:
    """Repository of educational explanations about XSS."""

    # General XSS concepts
    XSS_INTRO = """
Cross-Site Scripting (XSS) is a web security vulnerability that allows an attacker
to inject malicious scripts into web pages viewed by other users. XSS occurs when
a web application includes untrusted data without proper validation or escaping.

According to OWASP, there are three main types of XSS:
1. Reflected XSS - Script comes from the current HTTP request
2. Stored XSS - Script comes from the website's database
3. DOM-based XSS - Vulnerability exists in client-side code
"""

    # Reflected XSS
    REFLECTED_XSS_INTRO = """
[REFLECTED XSS]

Reflected XSS occurs when an application receives data in an HTTP request and
includes that data in the immediate response in an unsafe way.

How it works:
1. Attacker crafts a malicious URL containing JavaScript
2. Victim clicks the link (sent via email, social media, etc.)
3. Server reflects the malicious script back in the response
4. Victim's browser executes the script

Example vulnerable code:
    echo "You searched for: " . $_GET['search'];

If search="<script>alert(1)</script>", the script executes immediately.
"""

    REFLECTED_XSS_IMPACT = """
Impact of Reflected XSS:
- Session hijacking (stealing cookies/tokens)
- Credential theft (fake login forms)
- Defacement of web pages
- Redirection to malicious sites
- Keylogging and form grabbing
"""

    REFLECTED_XSS_PREVENTION = """
Reflected XSS remediation checklist:
1. Apply context-aware output encoding (HTML body, attribute, JavaScript, URL) using battle-tested libraries
   such as OWASP Java Encoder, Spring Security tags, or framework auto-escaping.
2. Normalize and strictly validate reflected parameters before rendering. Reject unexpected characters or limit
   length so payloads cannot smuggle angle brackets or quotes into the page.
3. Render responses through templating systems that auto-escape by default (Jinja2 autoescape, Handlebars,
   React) rather than concatenating strings manually.
4. When you must place data inside attributes, encode quotes (`"` → `&quot;`) and close the attribute before
   injecting user data so attackers cannot break out of the context.
5. Enforce a modern Content Security Policy (for example: `default-src 'self'; script-src 'self' 'nonce-random'`)
   to block inline JavaScript even if a reflection bug slips back in.
6. Set cookies with `HttpOnly`, `Secure`, and appropriate `SameSite` attributes to reduce the blast radius if
   an alert payload turns into a real session-stealing exploit.
7. Add automated tests or static analysis that diff rendered templates and fail builds when an output lacks
   escaping helpers, preventing regressions before they ship.
"""

    # Stored XSS
    STORED_XSS_INTRO = """
[STORED XSS]

Stored XSS (Persistent XSS) occurs when malicious script is stored on the target
server (in a database, message forum, comment field, etc.) and then displayed to
other users without proper sanitization.

How it works:
1. Attacker submits malicious script via input field (comment, profile, etc.)
2. Application stores the script in the database
3. When other users view the page, the script is retrieved and executed
4. Every visitor to that page becomes a victim

This is often more dangerous than reflected XSS because:
- No user interaction required (beyond viewing the page)
- Affects multiple users automatically
- Persists until removed from storage
"""

    STORED_XSS_IMPACT = """
Impact of Stored XSS:
- Mass credential harvesting
- Worm-like propagation (self-replicating XSS)
- Persistent backdoors
- Data exfiltration from all viewers
- Account takeover of multiple users
"""

    STORED_XSS_PREVENTION = """
Prevention for Stored XSS:
- Encode output on retrieval (not just on storage)
- Store data in its original form, encode on display
- Use parameterized queries to prevent SQL injection
- Implement strong Content Security Policy
- Regular security audits of stored content
"""

    # DOM-based XSS
    DOM_XSS_INTRO = """
[DOM-BASED XSS]

DOM-based XSS is a vulnerability where the attack payload is executed as a result
of modifying the DOM environment in the victim's browser. The server response does
not change, but the client-side code behaves unsafely.

How it works:
1. JavaScript reads from a controllable source (URL, window.location, etc.)
2. Data is written to a dangerous sink (innerHTML, eval, document.write, etc.)
3. If input contains executable code, it runs in the security context of the page

Example vulnerable code:
    var search = window.location.hash.substring(1);
    document.getElementById('result').innerHTML = search;

Key difference: The payload never goes to the server!
- Traditional XSS: Client → Server → Client (reflected/stored)
- DOM XSS: URL → Client JavaScript → DOM (never touches server)
"""

    DOM_XSS_SOURCES_SINKS = """
Common DOM XSS sources (attacker-controllable):
- window.location (href, search, hash, pathname)
- document.URL
- document.referrer
- window.name
- postMessage events

Common DOM XSS sinks (dangerous operations):
- innerHTML, outerHTML
- document.write(), document.writeln()
- eval(), setTimeout(), setInterval() with string arguments
- element.setAttribute()
- jQuery functions: html(), append(), etc.
"""

    DOM_XSS_PREVENTION = """
Prevention for DOM-based XSS:
- Avoid writing user-controllable data to dangerous sinks
- Use safe alternatives:
  * textContent instead of innerHTML
  * setAttribute() with validation
  * Avoid eval() entirely
- Encode data based on where it's being placed
- Use framework security features (React escaping, Angular sanitization)
- Implement strong CSP that blocks inline scripts
"""

    # Payload explanations
    PAYLOAD_BASIC_ALERT = """
Payload: <script>alert(1)</script>

This is the simplest XSS payload. It:
- Opens an alert box with the number "1"
- Proves JavaScript execution is possible
- Is often blocked by basic filters looking for <script> tags

Why it matters:
If alert(1) works, an attacker could run ANY JavaScript code:
- Steal cookies: document.cookie
- Make requests: fetch('/admin/delete', ...)
- Modify the page: document.body.innerHTML = ...
"""

    PAYLOAD_IMG_ONERROR = """
Payload: <img src=x onerror=alert(1)>

This payload uses an HTML event handler instead of <script> tags:
- <img> tag tries to load image from non-existent source "x"
- When loading fails, onerror event fires
- onerror handler executes JavaScript: alert(1)

Why it's useful:
- Bypasses filters that only block <script>
- Works in more contexts (attributes, some encoded scenarios)
- Demonstrates that ANY HTML tag with events can be dangerous
"""

    PAYLOAD_SVG_ONLOAD = """
Payload: <svg/onload=alert(1)>

This payload leverages SVG (Scalable Vector Graphics) tags:
- SVG is valid HTML5 element
- onload event fires when SVG element loads
- More compact than img tag

Why it's useful:
- Often missed by basic XSS filters
- Works without spaces (svg/onload vs svg onload)
- Can be shortened further for length-limited contexts
"""

    # Context explanations
    CONTEXT_HTML = """
[HTML Context]

When injecting into HTML body:
- Goal: Break out of text context and inject tags
- Look for: <tag>USER_INPUT</tag>
- Attack: Close current tag, inject malicious tag
- Example: </tag><script>alert(1)</script><tag>
"""

    CONTEXT_ATTRIBUTE = """
[HTML Attribute Context]

When injecting into tag attributes:
- Goal: Break out of attribute, add event handler
- Look for: <tag attr="USER_INPUT">
- Attack: Close attribute, inject event
- Example: " onload="alert(1)
- Result: <tag attr="" onload="alert(1)">
"""

    CONTEXT_JAVASCRIPT = """
[JavaScript Context]

When injecting into JavaScript code:
- Goal: Break out of string, execute arbitrary code
- Look for: var x = "USER_INPUT";
- Attack: Close string, add code
- Example: "; alert(1); //
- Result: var x = ""; alert(1); //";
"""

    # Filter evasion
    FILTER_EVASION_INTRO = """
[XSS Filter Evasion]

Web applications often implement filters to block XSS. Understanding why filters
fail teaches defense in depth:

Common naive filters:
1. Blacklisting <script> - dozens of other tags work
2. Blocking "javascript:" - event handlers work
3. Removing quotes - some contexts don't need them
4. Filtering alert() - use console.log, eval, etc.

The lesson: Blacklisting is insufficient. Use output encoding instead.
"""

    def get_explanation(self, key: str) -> str:
        """
        Get explanation by key.

        Args:
            key: Explanation key (attribute name)

        Returns:
            Explanation text or empty string if not found
        """
        return getattr(self, key, "")
