import hashlib
import os
import jwt
from datetime import datetime, timedelta
from typing import Any

# JWT配置
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "yuxi_know_secure_key")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION = 24 * 60 * 60  # 24小时过期

class AuthUtils:
    """认证工具类"""

    @staticmethod
    def hash_password(password: str) -> str:
        """使用SHA-256哈希密码"""
        # 生成盐
        salt = os.urandom(32).hex()
        # 哈希密码
        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        # 返回格式: "哈希值:盐"
        return f"{hashed}:{salt}"

    @staticmethod
    def verify_password(stored_password: str, provided_password: str) -> bool:
        """验证密码"""
        # 分离哈希值和盐
        if ":" not in stored_password:
            return False

        hashed, salt = stored_password.split(":")

        # 使用相同的盐哈希提供的密码
        check_hash = hashlib.sha256((provided_password + salt).encode()).hexdigest()

        # 比较哈希值
        return hashed == check_hash

    @staticmethod
    def create_access_token(data: dict[str, Any], expires_delta: timedelta | None = None) -> str:
        """创建JWT访问令牌"""
        to_encode = data.copy()

        # 设置过期时间
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(seconds=JWT_EXPIRATION)

        to_encode.update({"exp": expire})

        # 编码JWT
        #to_encode ：这是要编码到 JWT 载荷（payload）中的数据
        #JWT_SECRET_KEY：这是用于编码 JWT 的密钥，JWT 使用该密钥对 to_encode 数据进行签名，以确保令牌的完整性和防篡改性，该密钥应保持私密，不应泄露给客户端或其他服务。
        #algorithm=JWT_ALGORITHM，指定用于签名的算法。常见的算法有 HS256（对称加密）和 RS256（非对称加密）。
        encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
        return encoded_jwt

    @staticmethod
    def decode_token(token: str) -> dict[str, Any] | None:
        """解码验证JWT令牌"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.PyJWTError:
            return None

    @staticmethod
    def verify_access_token(token: str) -> dict[str, Any]:
        """验证访问令牌，如果无效则抛出异常"""
        try:
            payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("令牌已过期")
        except jwt.InvalidTokenError:
            raise ValueError("无效的令牌")
