import argparse
import json
from tqdm import tqdm

import sys
sys.path.append("./app/")

from app.settings import DBSettings
from sqlalchemy import create_engine
from app.db import SessionLocal
from app.db.models import TextSample
import uuid



def main():
    parser = argparse.ArgumentParser(description='Load data into DB.')
    parser.add_argument('--file-name', type=str)
    #parser.add_argument('save-frequency', type=int, default=100)
    args = parser.parse_args()

    db = SessionLocal()

    with open(args.file_name) as f:
        json_data = json.load(f)
    objects = [TextSample(text=str(item), id=str(uuid.uuid4().hex)) for item in json_data['data']]
    db.bulk_save_objects(objects)
    db.commit()
        
    #objects = []
    #with open(args.file_name) as f:
    #    for idx, line in tqdm(enumerate(f)):
    #        print(line)
    #        objects.append(TextSampleCreate(text=json.loads(line)))
    #        if (idx + 1) % 100 == 0 or idx == len(f) - 1:
    #            db.bulk_save_objects(objects)
    #            db.commit()
    #            objects.clear()

if __name__ == '__main__':
    main()