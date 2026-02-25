"""コンテンツのサニタイズ機能"""
import re
import os
from typing import List, Tuple, Dict, Optional


class Sanitizer:
    """機密情報をサニタイズするクラス"""

    def __init__(
        self,
        enable_auto_sanitize: bool = False,
        custom_replacements: Optional[List[Tuple[str, str]]] = None
    ):
        self.enable_auto_sanitize = enable_auto_sanitize
        self.custom_replacements = custom_replacements or []

    def sanitize(self, content: str) -> Tuple[str, Dict[str, int]]:
        """
        コンテンツから機密情報を置換

        Args:
            content: 元のコンテンツ

        Returns:
            (置換後のコンテンツ, 置換統計の辞書)
        """
        stats = {}

        # 自動サニタイズ
        if self.enable_auto_sanitize:
            content, stats = self._auto_sanitize(content, stats)

        # カスタム置換
        if self.custom_replacements:
            content, stats = self._custom_sanitize(content, stats)

        return content, stats

    def _auto_sanitize(self, content: str, stats: Dict[str, int]) -> Tuple[str, Dict[str, int]]:
        """自動サニタイズパターンを適用"""

        # IPv4アドレス
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        ips = re.findall(ip_pattern, content)
        for i, ip in enumerate(set(ips), 1):
            if not (ip.startswith('127.') or ip.startswith('0.') or 
                    ip.startswith('192.168.') or ip.startswith('10.')):
                content = content.replace(ip, f'[REDACTED_IP_{i}]')
                stats['IP addresses'] = stats.get('IP addresses', 0) + 1

        # AWS Access Key
        aws_key_pattern = r'\b((?:AKIA|ASIA)[0-9A-Z]{16})\b'
        aws_keys = re.findall(aws_key_pattern, content)
        for i, key in enumerate(set(aws_keys), 1):
            content = content.replace(key, f'[REDACTED_AWS_KEY_{i}]')
            stats['AWS Keys'] = stats.get('AWS Keys', 0) + 1

        # AWS Secret Access Key（文脈付きで誤爆を抑制）
        aws_secret_pattern = r'(?i)\b(aws_secret_access_key|secret_access_key)\b\s*[:=]\s*([A-Za-z0-9/+=]{40})'
        content, count = re.subn(
            aws_secret_pattern,
            r'\1=[REDACTED_AWS_SECRET]',
            content
        )
        if count:
            stats['AWS Secrets'] = stats.get('AWS Secrets', 0) + count

        # パスワード
        password_pattern = r'(password|passwd|pwd)[\s]*[=:]["\']?([^\s"\']{6,})["\']?'
        passwords = re.findall(password_pattern, content, re.IGNORECASE)
        for i, (pwd_type, pwd_value) in enumerate(set(passwords), 1):
            content = content.replace(pwd_value, f'[REDACTED_PASSWORD_{i}]')
            stats['Passwords'] = stats.get('Passwords', 0) + 1

        # URL内の資格情報 (user:pass@)
        url_cred_pattern = r'(?i)\b([a-z][a-z0-9+\-.]*://)([^:\s/@]+):([^@\s]+)@'
        content, count = re.subn(url_cred_pattern, r'\1\2:[REDACTED_URL_PASSWORD]@', content)
        if count:
            stats['URL Credentials'] = stats.get('URL Credentials', 0) + count

        # URLクエリのトークン
        url_token_pattern = r'(?i)([?&](?:access_token|token|api_key|apikey|auth|signature|sig|secret|key)=)([^&\s#]+)'
        content, count = re.subn(url_token_pattern, r'\1[REDACTED_QUERY_TOKEN]', content)
        if count:
            stats['URL Tokens'] = stats.get('URL Tokens', 0) + count

        # メールアドレス（URL内の user:pass@ を誤検出しないように注意）
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b'
        redacted_emails = 0
        for match in re.finditer(email_pattern, content):
            start = match.start()
            prev_char = content[start - 1] if start > 0 else ''
            prefix = content[max(0, start - 20):start]
            if prev_char == ':' and '://' in prefix:
                continue
            email = match.group(0)
            content = content.replace(email, f'[REDACTED_EMAIL_{redacted_emails + 1}]')
            redacted_emails += 1
        if redacted_emails:
            stats['Email addresses'] = stats.get('Email addresses', 0) + redacted_emails

        # API Key
        api_key_pattern = r'(?i)\b(api[_-]?key|apikey|api[_-]?secret|access[_-]?token|token|secret|auth[_-]?token)\b\s*[:=]\s*["\']?([A-Za-z0-9_\-]{20,})["\']?'
        api_keys = re.findall(api_key_pattern, content)
        for i, (_key_type, key_value) in enumerate(set(api_keys), 1):
            content = content.replace(key_value, f'[REDACTED_API_KEY_{i}]')
            stats['API Keys'] = stats.get('API Keys', 0) + 1

        # JWT
        jwt_pattern = r'\b(eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,})\b'
        content, count = re.subn(jwt_pattern, '[REDACTED_JWT]', content)
        if count:
            stats['JWTs'] = stats.get('JWTs', 0) + count

        # GitHub Tokens
        github_token_pattern = r'\b(ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{36}\b'
        content, count = re.subn(github_token_pattern, '[REDACTED_GH_TOKEN]', content)
        if count:
            stats['GitHub Tokens'] = stats.get('GitHub Tokens', 0) + count

        # GitLab PAT
        gitlab_token_pattern = r'\bglpat-[A-Za-z0-9\-_]{20,}\b'
        content, count = re.subn(gitlab_token_pattern, '[REDACTED_GITLAB_TOKEN]', content)
        if count:
            stats['GitLab Tokens'] = stats.get('GitLab Tokens', 0) + count

        # Slack Tokens
        slack_token_pattern = r'\bxox[baprs]-[0-9A-Za-z-]{10,}\b'
        content, count = re.subn(slack_token_pattern, '[REDACTED_SLACK_TOKEN]', content)
        if count:
            stats['Slack Tokens'] = stats.get('Slack Tokens', 0) + count

        # GCP API Key
        gcp_key_pattern = r'\bAIza[0-9A-Za-z\-_]{35}\b'
        content, count = re.subn(gcp_key_pattern, '[REDACTED_GCP_KEY]', content)
        if count:
            stats['GCP Keys'] = stats.get('GCP Keys', 0) + count

        # Bearer Token
        bearer_pattern = r'(?i)\bBearer\s+([A-Za-z0-9\-._~+/]+=*)'
        bearer_redacted = 0
        def _bearer_repl(match: re.Match) -> str:
            nonlocal bearer_redacted
            token = match.group(1)
            if len(token) < 20:
                return match.group(0)
            bearer_redacted += 1
            return "Bearer [REDACTED_BEARER]"
        content = re.sub(bearer_pattern, _bearer_repl, content)
        if bearer_redacted:
            stats['Bearer Tokens'] = stats.get('Bearer Tokens', 0) + bearer_redacted

        # DB接続文字列（user:password@）
        db_url_pattern = r'(?i)\b(postgres(?:ql)?|mysql|mariadb|mongodb(?:\+srv)?|mssql|redis)://([^:\s/]+):([^@\s]+)@'
        content, count = re.subn(db_url_pattern, r'\1://\2:[REDACTED_DB_PASSWORD]@', content)
        if count:
            stats['DB Credentials'] = stats.get('DB Credentials', 0) + count

        # Private key
        if '-----BEGIN PRIVATE KEY-----' in content or '-----BEGIN RSA PRIVATE KEY-----' in content or '-----BEGIN OPENSSH PRIVATE KEY-----' in content:
            private_key_pattern = r'-----BEGIN (?:RSA |OPENSSH )?PRIVATE KEY-----.*?-----END (?:RSA |OPENSSH )?PRIVATE KEY-----'
            content = re.sub(private_key_pattern, '[REDACTED_PRIVATE_KEY]', content, flags=re.DOTALL)
            stats['Private Keys'] = stats.get('Private Keys', 0) + 1

        return content, stats

    def _custom_sanitize(self, content: str, stats: Dict[str, int]) -> Tuple[str, Dict[str, int]]:
        """カスタム置換パターンを適用"""
        for pattern, replacement in self.custom_replacements:
            try:
                matches = re.findall(pattern, content)
                if matches:
                    content = re.sub(pattern, replacement, content)
                    stats[f'Custom: {pattern}'] = len(matches)
            except re.error:
                if pattern in content:
                    count = content.count(pattern)
                    content = content.replace(pattern, replacement)
                    stats[f'Custom: {pattern}'] = count

        return content, stats

    @staticmethod
    def load_replacement_patterns(replace_file_path: str) -> List[Tuple[str, str]]:
        """
        置換パターンファイルから置換ルールを読み込む

        Args:
            replace_file_path: 置換パターンファイルのパス

        Returns:
            (パターン, 置換後文字列) のタプルのリスト
        """
        patterns = []
        if not replace_file_path or not os.path.exists(replace_file_path):
            return patterns

        with open(replace_file_path, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                # 矢印形式
                if '->' in line:
                    parts = line.split('->', 1)
                    if len(parts) == 2:
                        pattern = parts[0].strip()
                        replacement = parts[1].strip()
                        patterns.append((pattern, replacement))
                        continue

                # スペース/タブ区切り
                parts = line.split(None, 1)
                if len(parts) == 2:
                    pattern = parts[0]
                    replacement = parts[1]
                    patterns.append((pattern, replacement))

        return patterns
