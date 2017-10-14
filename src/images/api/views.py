from itertools import product

from django.db.models import Count
from django.http import JsonResponse
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from src.albums.models import Album

from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, \
    get_object_or_404
from .serializers import ImageSerializer, CreateImageSerializer, DetailedImageSerializer
from src.images.models import Image
from src.profiles.models import Profile
from src.gallery.helpers import log, prepare_path

import ipdb


class GetAllImages(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Image.objects.filter(album_id=self.kwargs.get("album_id")) or Image.objects.all()


class GetImage(RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Image.objects.get(pk=self.kwargs.get("image_id"))


class GetImagesAPI(ListAPIView):
    """

    """
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name__icontains', 'description__icontains', 'tag__name__icontains', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self, *args, **kwargs):
        # ipdb.set_trace()
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            return Response({"status": "fail"}, status=403)

        profile = Profile.objects.get(pk=profile_id)

        if not profile:
            return Response({"status": "fail"}, status=404)

        album_id = self.kwargs.get("album_id")
        if not album_id:
            # return Image.objects.all()
            return Response({"status": "fail"}, status=403)

        album = profile.albums.get(pk=album_id)
        if not album:
            return Response({"status": "fail"}, status=404)

        queryset_list = album.images.all()
        return queryset_list


class CreateImageAPI(CreateAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = CreateImageSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        # ipdb.set_trace()
        name = request.POST.get('name', None)
        description = request.POST.get('description', None)
        is_public = bool(request.POST.get('is_public', None))
        image = request.FILES['image']
        album_id = request.POST.get('album_id', self.kwargs.get('album_id'))

        image = Image.objects.create(
            name=name,
            description=description,
            is_public=is_public,
            image=image,
            album_id=album_id
        )
        return JsonResponse(self.serializer_class(instance=image).data)


class ImageDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    """

    """
    queryset = Image.objects.all()
    serializer_class = DetailedImageSerializer
    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]  # FIXME: testiraj

    def get_object(self):
        album_id = self.kwargs.get("album_id")
        if not album_id:
            return Response({"status": "fail"}, status=403)
        album = Album.objects.get(pk=album_id)
        if not album:
            return Response({"status": "fail"}, status=404)

        image_id = self.kwargs.get("image_id")
        # return album.images.get(pk=image_id)
        return get_object_or_404(Image, pk=image_id, album_id=album_id)

    def put(self, request, *args, **kwargs):
        # TODO: ако се мења име слике, треба и на диску да се промени

        profile_id = self.kwargs.get("profile_id")
        album_id = self.kwargs.get("album_id")
        image_id = self.kwargs.get("image_id")

        if not profile_id or not album_id or not image_id:
            return Response({"status": "fail"}, status=406)

        profile = Profile.objects.get(pk=profile_id)

        if not profile:
            return Response({"status": "fail"}, status=404)

        album = profile.albums.get(pk=album_id)

        if not album:
            return Response({"status": "fail"}, status=404)

        image = album.images.get(pk=image_id)

        image.name = request.POST.get('name', image.name)
        image.description = request.POST.get('description', image.description)
        image.is_public = request.POST.get('is_public', image.is_public)
        image.image = request.FILES.get('image', image.image)
        image.album = request.POST.get('album', image.album)

        tags = request.POST.getlist('tags',image.tag_set.all())

        for tag in tags:
            try:
                image.tag_set.remove(tag)
                image.tag_set.add(tag)
            except:
                image.tag_set.add(tag)

        image.save()

        return JsonResponse(self.serializer_class(instance=image).data)


    def delete(self, request, *args, **kwargs):
        # користи се django-cleanup за брисање слике-датотеке
        return self.destroy(request, *args, **kwargs)


class GetTopImages(ListAPIView):
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        from src.gallery.settings import top_likes
        from src.likes.models import Like

        # ipdb.set_trace(context=5)
        # all_images = Image.objects.all()
        # queryset_dict = []
        # for img in all_images.values():
        #     likes_count = Like.objects.filter(image__pk=img['id']).count()
        #     if likes_count >= top_likes:
        #         img['album'] = img['album_id']
        #         del img['album_id']
        #         queryset_dict.append(img)
        # serializer = ImageSerializer(data=queryset_dict, many=True)
        # serializer.is_valid()

        # return serializer.data
        # return JsonResponse(serializer.data, safe=False)


        # queryset_list = Image.objects.filter(like_set__count=top_likes)

        queryset_list = Image.objects.annotate(like__count=Count('like__pk')).filter(like__count__gte=top_likes)

        return queryset_list


class GetOwnerImages(ListAPIView):
    serializer_class = ImageSerializer
    filter_backends = [SearchFilter]  # ово мора бити низ!
    search_fields = ('name', 'description', 'tag__name', 'timestamp', 'updated')
    ordering_fields = '__all__'
    lookup_field = 'image'
    permission_classes = [AllowAny]

    def get_queryset(self):
        # ipdb.set_trace(context=5)
        profile_id = self.kwargs.get("profile_id")
        if not profile_id:
            return ImageSerializer(None).data
        queryset = Image.objects.filter(album__owner__pk=profile_id)
        return queryset
