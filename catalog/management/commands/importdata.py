from django.core.management.base import BaseCommand
from django.conf import settings
from pathlib import Path
import json
from catalog.models import Platform
from catalog import tmdb as tmdb_module


class Command(BaseCommand):
    help = 'Import JSON files from data/ into the database (uses catalog.tmdb helpers)'

    def add_arguments(self, parser):
        parser.add_argument('--data-dir', dest='data_dir', default=None,
                            help='Path to data directory (defaults to <BASE_DIR>/data)')

    def handle(self, *args, **options):
        data_dir = options.get('data_dir') or (Path(settings.BASE_DIR) / 'data')
        data_dir = Path(data_dir)
        if not data_dir.exists():
            self.stderr.write(self.style.ERROR(f"Data directory not found: {data_dir}"))
            return

        files = sorted([p for p in data_dir.iterdir() if p.suffix.lower() == '.json'])
        if not files:
            self.stdout.write(self.style.WARNING('No JSON files found in data directory.'))
            return

        total_created = 0
        for f in files:
            name = f.stem  # e.g. netflix-movies
            parts = name.rsplit('-', 1)
            if len(parts) != 2:
                self.stdout.write(self.style.WARNING(f"Skipping file with unexpected name: {f.name}"))
                continue
            platform_slug, kind = parts
            kind = kind if kind in ('movies', 'series') else 'movies'

            # find or create platform
            platform, _ = Platform.objects.get_or_create(slug=platform_slug,
                                                         defaults={'name': platform_slug.replace('-', ' ').title()})

            # load JSON
            try:
                with open(f, 'r', encoding='utf-8') as fh:
                    items = json.load(fh)
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Failed to load {f.name}: {e}"))
                continue

            created = 0
            for it in items:
                try:
                    tmdb_module._create_or_update_title_from_item(platform, it, kind='movies' if kind == 'movies' else 'tv')
                    created += 1
                except Exception as e:
                    # don't stop on individual errors
                    self.stderr.write(self.style.WARNING(f"Error importing item id={it.get('id')}: {e}"))

            total_created += created
            self.stdout.write(self.style.SUCCESS(f"Imported {created} items from {f.name} into platform '{platform.slug}'"))

        self.stdout.write(self.style.SUCCESS(f"Import complete. Total items processed: {total_created}"))
