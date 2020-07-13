import csv
from time import sleep


class StatusService:
    image_container_ids = []
    inUse = False

    def __init__(self):
        print("init status service")
        StatusService.inUse = True
        with open('/opt/project/main/resources/data.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow("")
            csv_file.close()
        StatusService.inUse = False

    def read(self):
        StatusService.inUse = True
        StatusService.image_container_ids = []
        with open('/opt/project/main/resources/data.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                if row[0] and row[1]:
                    print(f'\t{row[0]},{row[1]}.')
                    StatusService.image_container_ids.append((row[0], row[1], row[2]))
                    line_count += 1
            print(f'Processed {line_count} lines.')
            csv_file.close()
        StatusService.inUse = False

    def write(self):
        StatusService.inUse = True
        with open('/opt/project/main/resources/data.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for image_container_id in StatusService.image_container_ids:
                csv_writer.writerow([image_container_id[0], image_container_id[1], image_container_id[2]])
            csv_file.close()
        StatusService.inUse = False

    def add_image_ids(self, image_id, container_id, project_id):
        StatusService.image_container_ids.append((image_id, container_id, project_id))
        while StatusService.inUse:
            sleep(0.10)
        self.write()

    def delete_by_image_id(self, container_id):
        for image_container_id in StatusService.image_container_ids:
            if image_container_id[0] == container_id:
                StatusService.image_container_ids.remove(image_container_id)
        while StatusService.inUse:
            sleep(0.10)
        self.write()

    def checkIfOtherImage(self, image_id):
        count = 0
        for image_container_id in StatusService.image_container_ids:
            if image_id == image_container_id[0]:
                count += 1
        return count
