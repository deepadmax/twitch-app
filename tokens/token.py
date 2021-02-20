import requests
import json
import time


class Token:
    def __init__(self):
        raise NotImplementedError()
    
    def __str__(self):
        """Get cached token.
        If token has expired, renew it beforehand
        """

        if time.time() >= self.expires_at:
            self.update()

        return self.token

    def update(self):
        """Request App token"""

        response = requests.post(self.url, params=self.params)
        
        content = json.loads(response.content)

        # Return error if there is one
        if 'status' in content:
            raise RuntimeError(
                f'Status {content["status"]}: {content["message"]}',
                status=content['status'],
                message=content['message']
            )

        self.expires_at = time.time() + content['expires_in']
        
        self.token = content['access_token']