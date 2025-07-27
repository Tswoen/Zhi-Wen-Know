from fastapi import APIRouter
from server.routers.chat_router import chat
from server.routers.data_router import data
from server.routers.base_router import base
from server.routers.auth_router import auth
# from server.routers.graph_router import graph

import os

router = APIRouter()
router.include_router(base)
router.include_router(chat)
router.include_router(data)
router.include_router(auth)
# router.include_router(graph)


os.environ["SILICONFLOW_API_KEY"] = "sk-mvjhwoypajnggqoasejoqumfaabvifdrvztgvmxdpdyukggy"
# print("SILICONFLOW_API_KEY: ", os.environ["SILICONFLOW_API_KEY"])
print("DASHSCOPE_API_KEY: ", os.environ["DASHSCOPE_API_KEY"])
