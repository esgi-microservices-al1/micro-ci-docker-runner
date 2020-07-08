import csv


class StatusService:
    image_container_ids = []

    def __init__(self):
        # open('resources/data.csv', 'w+')
        print("init status service")

    def read(self):
        StatusService.image_container_ids = []
        with open('resources/data.csv', mode='r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=';')
            line_count = 0
            for row in csv_reader:
                print(f'\t{row[0]},{row[1]}.')
                StatusService.image_container_ids.append((row[0], row[1], row[2]))
                line_count += 1
            print(f'Processed {line_count} lines.')
            csv_file.close()

    def write(self):
        with open('resources/data.csv', mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for image_container_id in StatusService.image_container_ids:
                csv_writer.writerow([image_container_id[0], image_container_id[1], image_container_id[2]])
            csv_file.close()

    def add_image_ids(self, image_id, container_id, project_id):
        StatusService.image_container_ids.append((image_id, container_id, project_id))
        self.write()

    def delete_by_image_id(self, container_id):
        for image_container_id in StatusService.image_container_ids:
            if image_container_id[0] == container_id:
                StatusService.image_container_ids.remove(image_container_id)
        self.write()
