PGDMP  4    -                }            gis    17.4    17.4     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false            �           1262    16388    gis    DATABASE     i   CREATE DATABASE gis WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'ko-KR';
    DROP DATABASE gis;
                     postgres    false                        3079    16389    postgis 	   EXTENSION     ;   CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;
    DROP EXTENSION postgis;
                        false            �           0    0    EXTENSION postgis    COMMENT     ^   COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';
                             false    2            �            1259    17486    geo_features    TABLE     �   CREATE TABLE public.geo_features (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    geom public.geometry(Geometry,4326),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
     DROP TABLE public.geo_features;
       public         heap r       postgres    false    2    2    2    2    2    2    2    2            �            1259    17485    geo_features_id_seq    SEQUENCE     �   CREATE SEQUENCE public.geo_features_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.geo_features_id_seq;
       public               postgres    false    226            �           0    0    geo_features_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.geo_features_id_seq OWNED BY public.geo_features.id;
          public               postgres    false    225            �            1259    17470    places    TABLE     �   CREATE TABLE public.places (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description text,
    location public.geometry(Point,4326),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);
    DROP TABLE public.places;
       public         heap r       postgres    false    2    2    2    2    2    2    2    2            �            1259    17469    places_id_seq    SEQUENCE     �   CREATE SEQUENCE public.places_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 $   DROP SEQUENCE public.places_id_seq;
       public               postgres    false    224            �           0    0    places_id_seq    SEQUENCE OWNED BY     ?   ALTER SEQUENCE public.places_id_seq OWNED BY public.places.id;
          public               postgres    false    223                       2604    17489    geo_features id    DEFAULT     r   ALTER TABLE ONLY public.geo_features ALTER COLUMN id SET DEFAULT nextval('public.geo_features_id_seq'::regclass);
 >   ALTER TABLE public.geo_features ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    226    225    226                       2604    17473 	   places id    DEFAULT     f   ALTER TABLE ONLY public.places ALTER COLUMN id SET DEFAULT nextval('public.places_id_seq'::regclass);
 8   ALTER TABLE public.places ALTER COLUMN id DROP DEFAULT;
       public               postgres    false    223    224    224            �          0    17486    geo_features 
   TABLE DATA           O   COPY public.geo_features (id, name, description, geom, created_at) FROM stdin;
    public               postgres    false    226   $       �          0    17470    places 
   TABLE DATA           M   COPY public.places (id, name, description, location, created_at) FROM stdin;
    public               postgres    false    224   A                 0    16711    spatial_ref_sys 
   TABLE DATA           X   COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
    public               postgres    false    219   �       �           0    0    geo_features_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.geo_features_id_seq', 1, false);
          public               postgres    false    225            �           0    0    places_id_seq    SEQUENCE SET     ;   SELECT pg_catalog.setval('public.places_id_seq', 1, true);
          public               postgres    false    223            %           2606    17494    geo_features geo_features_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.geo_features
    ADD CONSTRAINT geo_features_pkey PRIMARY KEY (id);
 H   ALTER TABLE ONLY public.geo_features DROP CONSTRAINT geo_features_pkey;
       public                 postgres    false    226            #           2606    17478    places places_pkey 
   CONSTRAINT     P   ALTER TABLE ONLY public.places
    ADD CONSTRAINT places_pkey PRIMARY KEY (id);
 <   ALTER TABLE ONLY public.places DROP CONSTRAINT places_pkey;
       public                 postgres    false    224            �      x������ � �      �      x�-���0Fk{
/ �;�]l��(�4�KtY��8v���^�އ���?���;_����y<^�Λ�u��\�PF0�S ]��!9ӄd����-x�G�I�  S����t�P7ַ�佖R�\'.�            x������ � �     