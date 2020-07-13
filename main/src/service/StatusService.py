import csv
import os
from time import sleep


# while StatusService.inUse:
#   sleep(0.10)


class StatusService:
    image_container_ids = []
    inUse = False
    path = "/lockdir"

    def __init__(self):
        print("init status service")
        open('/opt/project/main/resources/data.csv', 'w').close()

    def read(self):

        image_container_ids_array = []
        with open('/opt/project/main/resources/data.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if row[0] and row[1]:
                    print(f'\t{row[0]},{row[1]}.')
                    image_container_ids_array.append((row[0], row[1], row[2], row[3]))
                    line_count += 1
            print(f'Processed {line_count} lines.')
            csv_file.close()
        StatusService.inUse = False
        return image_container_ids_array

    def write(self):
        with open('/opt/project/main/resources/data.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for image_container_id in StatusService.image_container_ids:
                csv_writer.writerow(
                    [image_container_id[0], image_container_id[1], image_container_id[2], image_container_id[3]])
            csv_file.close()

    def add_image_ids(self, image_id, container_id, project_id, date_created):

        while os.path.exists(self.path):
            sleep(0.10)
        os.mkdir(self.path)

        StatusService.image_container_ids = self.read()
        StatusService.image_container_ids.append((image_id, container_id, project_id, str(date_created)))

        self.write()

        os.rmdir(self.path)

    def delete_by_image_id(self, container_id):

        while os.path.exists(self.path):
            sleep(0.10)
        os.mkdir(self.path)

        StatusService.image_container_ids = self.read()
        for image_container_id in StatusService.image_container_ids:
            if image_container_id[0] == container_id:
                StatusService.image_container_ids.remove(image_container_id)
        self.write()

        os.rmdir(self.path)

    def checkIfOtherImage(self, image_id):

        while os.path.exists(self.path):
            sleep(0.10)
        os.mkdir(self.path)

        count = 0
        for image_container_id in StatusService.image_container_ids:
            if image_id == image_container_id[0]:
                count += 1
        os.rmdir(self.path)
        return count
