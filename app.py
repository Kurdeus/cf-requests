from DrissionPage import ChromiumPage
import requests
import time


class cf_bypass:
    def __init__(self, max_retries: int = -1, log: bool = True):
        self.driver = ChromiumPage()
        self.max_retries = max_retries
        self.log = log

    def _search_element_in_shadow(self, element, tag_type):
        """Search for an element of specified tag type within shadow roots."""
        # Check if element has shadow root with the target tag
        if element.shadow_root:
            if tag_type == "iframe" and element.shadow_root.child().tag == "iframe":
                return element.shadow_root.child()
            elif tag_type == "input" and element.shadow_root.ele("tag:input"):
                return element.shadow_root.ele("tag:input")
        
        # Recursively search in children
        for child in element.children():
            result = self._search_element_in_shadow(child, tag_type)
            if result:
                return result
        return None

    def _locate_verification_button(self):
        """Locate the Cloudflare verification button."""
        # Try direct search first
        inputs = self.driver.eles("tag:input")
        for input_ele in inputs:
            attrs = input_ele.attrs
            if "name" in attrs and "type" in attrs:
                if "turnstile" in attrs["name"] and attrs["type"] == "hidden":
                    return input_ele.parent().shadow_root.child()("tag:body").shadow_root("tag:input")

        # Fall back to recursive search
        self._log("Basic search failed. Searching recursively.")
        body = self.driver.ele("tag:body")
        iframe = self._search_element_in_shadow(body, "iframe")
        if iframe:
            return self._search_element_in_shadow(iframe("tag:body"), "input")
        
        self._log("Iframe not found. Button search failed.")
        return None

    def _log(self, message: str):
        """Log messages if logging is enabled."""
        if self.log:
            print(message)

    def _is_verification_bypassed(self) -> bool:
        """Check if the Cloudflare verification page is bypassed."""
        try:
            return "just a moment" not in self.driver.title.lower()
        except Exception as e:
            self._log(f"Error checking page title: {e}")
            return False

    def _bypass(self):
        """Attempt to bypass Cloudflare verification."""
        attempt = 0
        while not self._is_verification_bypassed():
            if 0 < self.max_retries <= attempt:
                self._log("Exceeded maximum retries. Bypass failed.")
                break

            self._log(f"Attempt {attempt + 1}: Trying to bypass...")
            try:
                button = self._locate_verification_button()
                if button:
                    self._log("Verification button found. Clicking.")
                    button.click()
                else:
                    self._log("Verification button not found.")
            except Exception as e:
                self._log(f"Error clicking button: {e}")
            
            attempt += 1
            time.sleep(2)

        self._log("Bypass " + ("successful" if self._is_verification_bypassed() else "failed"))

    def _get_cookie(self, url: str) -> str:
        """Bypass Cloudflare protection and return cookies."""
        try:
            self.driver.get(url)
            self._bypass()
            return self.driver.cookies().as_str()
        finally:
            self.driver.close()

    def bypass_cloudflare(self, url: str, session: requests.Session = None) -> requests.Session:
        """Return a requests session with bypassed Cloudflare cookies."""
        session.headers.update({
            "cookie": self._get_cookie(url),
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36"
        })
        return session
    

if __name__ == "__main__":

    url = "https://example.com/"


    bypasser = cf_bypass()
    session = requests.Session()
    bypasser.bypass_cloudflare(url, session)

    # now we have safe session for bypassing cloudflare bot protection
    response = session.get(url)
    print(response.text)
