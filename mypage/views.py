from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import FileResponse
from PIL import Image
import uuid
import os
from django.conf import settings
from io import BytesIO

class ColorModifiedPhotoView(APIView):
    def get(self, request, pk):
        try:
            uid = uuid.UUID(str(pk))
        except ValueError:
            return Response({"detail": "Invalid UUID"}, status=status.HTTP_400_BAD_REQUEST)

        # UUID 첫 자리로 이미지 선택
        hex_digit = int(str(uid)[0], 16)
        image_index = hex_digit % 3 + 1
        image_path = os.path.join(settings.BASE_DIR, "farm/files", f"photo{image_index}.png")

        if not os.path.exists(image_path):
            return Response({"detail": f"Image not found: photo{image_index}.png"}, status=status.HTTP_404_NOT_FOUND)

        try:
            with Image.open(image_path).convert("RGBA") as img:
                # ✅ 이미지 크기 축소 (예: 너비 256px 기준)
                base_width = 256
                w_percent = base_width / float(img.width)
                h_size = int((float(img.height) * float(w_percent)))
                img = img.resize((base_width, h_size), Image.LANCZOS)

                # ✅ 색상 보정 제거됨

                buffer = BytesIO()
                img.save(buffer, format="PNG")
                buffer.seek(0)

                return FileResponse(buffer, content_type="image/png")
        except Exception as e:
            return Response({"detail": f"Image processing failed: {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
